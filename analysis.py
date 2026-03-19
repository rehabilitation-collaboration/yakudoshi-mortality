"""
Statistical analysis of yakudoshi (unlucky years) and mortality.

Primary analysis: Negative binomial regression with cubic regression splines.
Secondary analysis: Local residual method (continuity with original project).
Sensitivity analyses: Multiple robustness checks.
"""

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.genmod.generalized_linear_model import GLM
from statsmodels.genmod.families import Poisson, NegativeBinomial
from patsy import dmatrix

from data_loader import load_mortality_long, filter_analysis_range, get_data_summary
from definitions import (
    AGE_MIN, AGE_MAX, NEIGHBOR_WINDOW,
    get_yakudoshi_ages, get_yakudoshi_with_mae_ato,
    YAKUDOSHI_MANNENREI, YAKUDOSHI_WITH_MAE_ATO,
)


# --- Primary Analysis: Negative Binomial Regression ---

def estimate_nb_alpha(df: pd.DataFrame, spline_df: int = 5) -> float:
    """Estimate NB2 dispersion parameter alpha by two-stage AIC grid search.

    Stage 1: Coarse search over log10(alpha) in [-4, 2] with step 0.5.
    Stage 2: Fine search around the coarse optimum with step 0.05.

    Alpha is estimated from a null model (without the yakudoshi indicator)
    to avoid circularity in the primary analysis.

    Args:
        df: DataFrame with Deaths, Exposures, Age, Year columns.
        spline_df: Degrees of freedom for the age spline.

    Returns:
        Estimated alpha value.
    """
    df = df.copy()
    df = df[df["Exposures"] > 0].copy()
    df["log_exposure"] = np.log(df["Exposures"])
    formula_rhs = f"cr(Age, df={spline_df}) + cr(Year, df=3)"
    X = dmatrix(formula_rhs, data=df, return_type="dataframe")

    def _fit_alpha(alpha):
        try:
            model = GLM(df["Deaths"], X, family=NegativeBinomial(alpha=alpha),
                        offset=df["log_exposure"])
            return model.fit().aic
        except Exception:
            return np.inf

    # Stage 1: coarse search
    best_alpha = 1.0
    best_aic = np.inf
    for log_alpha in np.arange(-4, 2.5, 0.5):
        alpha = 10 ** log_alpha
        aic = _fit_alpha(alpha)
        if aic < best_aic:
            best_aic = aic
            best_alpha = alpha

    # Stage 2: fine search around coarse optimum
    coarse_log = np.log10(best_alpha)
    for log_alpha in np.arange(coarse_log - 0.5, coarse_log + 0.55, 0.05):
        alpha = 10 ** log_alpha
        aic = _fit_alpha(alpha)
        if aic < best_aic:
            best_aic = aic
            best_alpha = alpha

    return best_alpha


def fit_regression_model(df: pd.DataFrame, yakudoshi_ages: list[int],
                         spline_df: int = 5, family: str = "nb",
                         nb_alpha: float | None = None) -> dict:
    """Fit GLM regression: Deaths ~ cr(Age, df) + Yakudoshi + cr(Year, 3).

    Args:
        df: Long-format DataFrame with Deaths, Exposures, Age, Year columns.
            Must be filtered to a single sex.
        yakudoshi_ages: List of yakudoshi ages (mannenrei).
        spline_df: Degrees of freedom for cubic regression spline on age.
        family: "nb" for Negative Binomial (primary), "poisson" for Poisson (sensitivity).
        nb_alpha: NB dispersion parameter. If None and family="nb", estimated by AIC grid search.

    Returns:
        Dict with model results including IRR, CI, p-value, overdispersion diagnostics.
    """
    df = df.copy()
    df = df[df["Exposures"] > 0].copy()
    df["yakudoshi"] = df["Age"].isin(yakudoshi_ages).astype(int)
    df["log_exposure"] = np.log(df["Exposures"])

    # Cubic regression spline for age + spline for year (nonlinear trend) + yakudoshi
    formula_rhs = f"cr(Age, df={spline_df}) + yakudoshi + cr(Year, df=3)"
    X = dmatrix(formula_rhs, data=df, return_type="dataframe")

    if family == "nb":
        if nb_alpha is None:
            nb_alpha = estimate_nb_alpha(df, spline_df)
        glm_family = NegativeBinomial(alpha=nb_alpha)
    else:
        glm_family = Poisson()
        nb_alpha = None

    model = GLM(
        df["Deaths"],
        X,
        family=glm_family,
        offset=df["log_exposure"],
    )
    result = model.fit()

    # Extract yakudoshi coefficient
    yaku_idx = [i for i, name in enumerate(X.columns) if name == "yakudoshi"][0]
    coef = result.params.iloc[yaku_idx]
    se = result.bse.iloc[yaku_idx]
    p_value = result.pvalues.iloc[yaku_idx]
    ci_low, ci_high = result.conf_int().iloc[yaku_idx]

    irr = np.exp(coef)
    irr_ci_low = np.exp(ci_low)
    irr_ci_high = np.exp(ci_high)

    # Overdispersion diagnostic
    deviance_ratio = result.deviance / result.df_resid if result.df_resid > 0 else np.nan

    return {
        "coefficient": coef,
        "se": se,
        "irr": irr,
        "irr_ci_low": irr_ci_low,
        "irr_ci_high": irr_ci_high,
        "p_value": p_value,
        "aic": result.aic,
        "deviance": result.deviance,
        "df_resid": result.df_resid,
        "deviance_ratio": deviance_ratio,
        "nb_alpha": nb_alpha,
        "n_obs": len(df),
        "spline_df": spline_df,
        "family": family,
        "model_result": result,
    }


def fit_per_age(df: pd.DataFrame, yakudoshi_ages: list[int],
                spline_df: int = 5, family: str = "nb",
                nb_alpha: float | None = None) -> list[dict]:
    """Fit regression for each individual yakudoshi age."""
    # Estimate alpha once for all per-age models (same data)
    if family == "nb" and nb_alpha is None:
        nb_alpha = estimate_nb_alpha(df, spline_df)

    results = []
    for yaku_age in yakudoshi_ages:
        df_copy = df.copy()
        df_copy = df_copy[df_copy["Exposures"] > 0].copy()
        df_copy["yakudoshi"] = (df_copy["Age"] == yaku_age).astype(int)
        df_copy["log_exposure"] = np.log(df_copy["Exposures"])

        formula_rhs = f"cr(Age, df={spline_df}) + yakudoshi + cr(Year, df=3)"
        X = dmatrix(formula_rhs, data=df_copy, return_type="dataframe")

        if family == "nb":
            glm_family = NegativeBinomial(alpha=nb_alpha)
        else:
            glm_family = Poisson()

        model = GLM(
            df_copy["Deaths"],
            X,
            family=glm_family,
            offset=df_copy["log_exposure"],
        )
        result = model.fit()

        yaku_idx = [i for i, name in enumerate(X.columns) if name == "yakudoshi"][0]
        coef = result.params.iloc[yaku_idx]
        ci_low, ci_high = result.conf_int().iloc[yaku_idx]

        results.append({
            "age": yaku_age,
            "irr": np.exp(coef),
            "irr_ci_low": np.exp(ci_low),
            "irr_ci_high": np.exp(ci_high),
            "p_value": result.pvalues.iloc[yaku_idx],
        })

    return results


def select_spline_df(df: pd.DataFrame, yakudoshi_ages: list[int],
                     df_values: tuple = (3, 4, 5, 6, 7, 8, 9),
                     family: str = "nb") -> dict:
    """Select optimal spline df by AIC.

    Returns:
        Dict with per-df results and the optimal df.
    """
    results = {}
    for df_val in df_values:
        r = fit_regression_model(df, yakudoshi_ages, spline_df=df_val, family=family)
        results[df_val] = r

    best_df = min(results, key=lambda k: results[k]["aic"])
    return {"per_df": results, "best_df": best_df, "best_aic": results[best_df]["aic"]}


# --- Secondary Analysis: Local Residual Method ---

def compute_local_residuals(mx_series: pd.Series, ages: pd.Series,
                            window: int = NEIGHBOR_WINDOW) -> pd.Series:
    """Compute local residuals: log(Mx) - mean(log(Mx) of neighbors).

    Args:
        mx_series: Mortality rates (positionally aligned with ages).
        ages: Corresponding ages (positionally aligned with mx_series).
        window: Number of neighboring ages on each side.

    Returns:
        Series of residuals (same index as input).
    """
    mx_vals = mx_series.values
    age_vals = ages.values
    log_mx = np.log(mx_vals)
    residuals = np.full(len(log_mx), np.nan)

    unique_ages = sorted(set(age_vals))
    age_to_positions = {}
    for a in unique_ages:
        age_to_positions[a] = np.where(age_vals == a)[0]

    for a in unique_ages:
        neighbor_ages = [na for na in unique_ages
                         if na != a and abs(na - a) <= window]
        if not neighbor_ages:
            continue

        neighbor_positions = np.concatenate(
            [age_to_positions[na] for na in neighbor_ages]
        )
        neighbor_mean = np.mean(log_mx[neighbor_positions])

        for pos in age_to_positions[a]:
            residuals[pos] = log_mx[pos] - neighbor_mean

    return pd.Series(residuals, index=mx_series.index)


def evaluate_local_residuals(df: pd.DataFrame, yakudoshi_ages: list[int],
                         window: int = NEIGHBOR_WINDOW) -> dict:
    """Test yakudoshi effect using local residual method across all years."""
    all_residuals = []
    all_is_yaku = []

    for year in sorted(df["Year"].unique()):
        year_df = df[df["Year"] == year].sort_values("Age").reset_index(drop=True)
        year_df = year_df.dropna(subset=["Mx"])
        if len(year_df) < 10:
            continue

        resid = compute_local_residuals(year_df["Mx"], year_df["Age"], window)

        for i, val in enumerate(resid):
            if np.isnan(val):
                continue
            age = year_df.iloc[i]["Age"]
            all_residuals.append(val)
            all_is_yaku.append(age in yakudoshi_ages)

    all_residuals = np.array(all_residuals)
    all_is_yaku = np.array(all_is_yaku)

    yaku_resid = all_residuals[all_is_yaku]
    non_yaku_resid = all_residuals[~all_is_yaku]

    # One-sample Wilcoxon signed-rank test (yakudoshi residuals > 0)
    if len(yaku_resid) >= 2:
        try:
            stat_w, p_wilcoxon = stats.wilcoxon(yaku_resid, alternative="greater")
        except ValueError:
            stat_w, p_wilcoxon = np.nan, np.nan
    else:
        stat_w, p_wilcoxon = np.nan, np.nan

    # Mann-Whitney U test (yakudoshi > non-yakudoshi)
    stat_u, p_mannwhitney = stats.mannwhitneyu(
        yaku_resid, non_yaku_resid, alternative="greater"
    )

    # Permutation test
    observed_mean = np.mean(yaku_resid)
    n_yaku = len(yaku_resid)
    rng = np.random.default_rng(42)
    n_perm = 100_000
    perm_means = np.array([
        np.mean(rng.choice(all_residuals, size=n_yaku, replace=False))
        for _ in range(n_perm)
    ])
    p_perm = np.mean(perm_means >= observed_mean)

    # Cohen's d (two-group: yaku vs non-yaku)
    mean_diff = np.mean(yaku_resid) - np.mean(non_yaku_resid)
    n1, n2 = len(yaku_resid), len(non_yaku_resid)
    var1, var2 = np.var(yaku_resid, ddof=1), np.var(non_yaku_resid, ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    cohens_d = mean_diff / pooled_sd if pooled_sd > 0 else 0

    return {
        "n_yakudoshi_obs": n_yaku,
        "n_non_yakudoshi_obs": len(non_yaku_resid),
        "mean_yaku_residual": observed_mean,
        "mean_non_yaku_residual": np.mean(non_yaku_resid),
        "p_wilcoxon": p_wilcoxon,
        "p_mannwhitney": p_mannwhitney,
        "p_permutation": p_perm,
        "cohens_d": cohens_d,
    }


# --- Sensitivity Analyses ---

def sensitivity_kazoedoshi_offset(df: pd.DataFrame, sex: str,
                                  spline_df: int = 5, nb_alpha: float | None = None,
                                  include_mae_ato: bool = False) -> dict[int, dict]:
    """Test with different kazoedoshi-to-mannenrei offsets (1 and 2)."""
    results = {}
    for offset in (1, 2):
        if include_mae_ato:
            ages = get_yakudoshi_with_mae_ato(sex, offset)
        else:
            ages = get_yakudoshi_ages(sex, offset)
        results[offset] = fit_regression_model(df, ages, spline_df=spline_df, nb_alpha=nb_alpha)
    return results


def sensitivity_spline_df(df: pd.DataFrame, yakudoshi_ages: list[int],
                          df_values: tuple = (3, 5, 7, 9),
                          nb_alpha: float | None = None) -> dict[int, dict]:
    """Test with different spline degrees of freedom.

    Args:
        nb_alpha: If provided, alpha is held constant across all df values
                  to isolate the spline effect. If None, alpha is re-estimated
                  per df value.
    """
    return {df_val: fit_regression_model(df, yakudoshi_ages, spline_df=df_val,
                                          nb_alpha=nb_alpha)
            for df_val in df_values}


def sensitivity_era(df: pd.DataFrame, yakudoshi_ages: list[int],
                    spline_df: int = 5) -> dict[str, dict]:
    """Test by historical era. Alpha is re-estimated per era (different data)."""
    eras = {
        "postwar (1947-1960)": (1947, 1960),
        "growth (1961-1990)": (1961, 1990),
        "modern (1991-2024)": (1991, 2024),
    }
    results = {}
    for era_name, (y_min, y_max) in eras.items():
        era_df = df[(df["Year"] >= y_min) & (df["Year"] <= y_max)]
        if len(era_df) > 0:
            results[era_name] = fit_regression_model(era_df, yakudoshi_ages, spline_df=spline_df)
    return results


def sensitivity_age_range(df_full: pd.DataFrame, yakudoshi_ages: list[int],
                          spline_df: int = 5) -> dict[str, dict]:
    """Test with different age ranges. Alpha is re-estimated per range (different data)."""
    ranges = {
        "15-80 (primary)": (15, 80),
        "20-70 (narrow)": (20, 70),
        "15-90 (wide)": (15, 90),
    }
    results = {}
    for label, (a_min, a_max) in ranges.items():
        range_df = filter_analysis_range(df_full, a_min, a_max)
        valid_ages = [a for a in yakudoshi_ages if a_min <= a <= a_max]
        if valid_ages:
            results[label] = fit_regression_model(range_df, valid_ages, spline_df=spline_df)
    return results


def sensitivity_poisson_vs_nb(df: pd.DataFrame, yakudoshi_ages: list[int],
                              spline_df: int = 5,
                              nb_alpha: float | None = None) -> dict[str, dict]:
    """Compare Poisson vs Negative Binomial results using same spline df."""
    return {
        "poisson": fit_regression_model(df, yakudoshi_ages, spline_df=spline_df, family="poisson"),
        "negative_binomial": fit_regression_model(df, yakudoshi_ages, spline_df=spline_df,
                                                   nb_alpha=nb_alpha),
    }


def sensitivity_residual_window(df: pd.DataFrame, yakudoshi_ages: list[int],
                                windows: tuple = (2, 3, 4, 5)) -> dict[int, dict]:
    """Test local residual method with different neighbor window sizes."""
    return {w: evaluate_local_residuals(df, yakudoshi_ages, window=w) for w in windows}


# --- Main Runner ---

def run_full_analysis() -> dict:
    """Run the complete analysis pipeline."""
    print("Loading JMD data...")
    df_long = load_mortality_long()
    df = filter_analysis_range(df_long, AGE_MIN, AGE_MAX)

    summary = get_data_summary(df)
    print(f"Data: {summary['n_years']} years ({summary['year_range'][0]}-{summary['year_range'][1]})")
    print(f"Age range: {AGE_MIN}-{AGE_MAX}")
    print(f"Missing Mx values: {summary['n_missing_mx']}")
    print()

    results = {"data_summary": summary}

    for sex in ("male", "female"):
        print(f"=== {sex.upper()} ===")
        sex_df = df[df["Sex"] == sex].copy()
        yaku_ages = YAKUDOSHI_MANNENREI[sex]
        yaku_ages_mae_ato = YAKUDOSHI_WITH_MAE_ATO[sex]

        print(f"Yakudoshi ages (mannenrei): {yaku_ages}")
        print(f"With mae/ato-yaku: {yaku_ages_mae_ato}")
        print()

        sex_results = {}

        # AIC-based spline df selection
        print("  [Model selection] AIC-based spline df...")
        df_selection = select_spline_df(sex_df, yaku_ages)
        best_df = df_selection["best_df"]
        print(f"    Best df = {best_df} (AIC = {df_selection['best_aic']:.1f})")
        for df_val, r in df_selection["per_df"].items():
            marker = " <-- best" if df_val == best_df else ""
            print(f"    df={df_val}: AIC={r['aic']:.1f}{marker}")
        sex_results["df_selection"] = {
            "best_df": best_df,
            "aic_per_df": {k: v["aic"] for k, v in df_selection["per_df"].items()},
        }
        print()

        # Overdispersion diagnostic (Poisson)
        print("  [Overdispersion] Poisson deviance/df_resid...")
        poisson_check = fit_regression_model(sex_df, yaku_ages, spline_df=best_df, family="poisson")
        print(f"    Deviance/df_resid = {poisson_check['deviance_ratio']:.2f} (>>1 = overdispersion)")
        sex_results["overdispersion_ratio"] = poisson_check["deviance_ratio"]

        # Estimate NB alpha once for this sex (reuse across all NB models)
        print("  [Alpha estimation] NB alpha by AIC grid search...")
        estimated_alpha = estimate_nb_alpha(sex_df, best_df)
        print(f"    Estimated alpha = {estimated_alpha:.6f}")
        sex_results["nb_alpha"] = estimated_alpha

        # Primary: NB regression (hon-yaku only)
        print(f"  [Primary] NB regression (hon-yaku, df={best_df}, alpha={estimated_alpha:.6f})...")
        primary = fit_regression_model(sex_df, yaku_ages, spline_df=best_df, nb_alpha=estimated_alpha)
        print(f"    IRR = {primary['irr']:.4f} ({primary['irr_ci_low']:.4f}-{primary['irr_ci_high']:.4f})")
        print(f"    p = {primary['p_value']:.4f}")
        print(f"    Deviance/df = {primary['deviance_ratio']:.2f}")
        sex_results["primary_hon_yaku"] = primary

        # Primary: NB regression (with mae/ato-yaku)
        print(f"  [Primary] NB regression (with mae/ato-yaku, df={best_df})...")
        primary_mae_ato = fit_regression_model(sex_df, yaku_ages_mae_ato, spline_df=best_df, nb_alpha=estimated_alpha)
        print(f"    IRR = {primary_mae_ato['irr']:.4f} ({primary_mae_ato['irr_ci_low']:.4f}-{primary_mae_ato['irr_ci_high']:.4f})")
        print(f"    p = {primary_mae_ato['p_value']:.4f}")
        sex_results["primary_mae_ato"] = primary_mae_ato

        # Per-age analysis
        print("  [Per-age] Individual yakudoshi ages (NB)...")
        per_age = fit_per_age(sex_df, yaku_ages, spline_df=best_df, nb_alpha=estimated_alpha)
        for r in per_age:
            print(f"    Age {r['age']}: IRR = {r['irr']:.4f} ({r['irr_ci_low']:.4f}-{r['irr_ci_high']:.4f}), p = {r['p_value']:.4f}")
        sex_results["per_age"] = per_age

        # Secondary: Local residual method
        print("  [Secondary] Local residual method...")
        resid_hon = evaluate_local_residuals(sex_df, yaku_ages)
        print(f"    Mean residual (yaku): {resid_hon['mean_yaku_residual']:+.6f}")
        print(f"    Mean residual (non-yaku): {resid_hon['mean_non_yaku_residual']:+.6f}")
        print(f"    p(permutation) = {resid_hon['p_permutation']:.4f}")
        print(f"    Cohen's d = {resid_hon['cohens_d']:+.4f}")
        sex_results["residual_hon_yaku"] = resid_hon

        resid_mae_ato = evaluate_local_residuals(sex_df, yaku_ages_mae_ato)
        sex_results["residual_mae_ato"] = resid_mae_ato

        # Sensitivity: Poisson vs NB comparison (same spline df and alpha as primary)
        print("  [Sensitivity] Poisson vs Negative Binomial...")
        sens_family = sensitivity_poisson_vs_nb(sex_df, yaku_ages, spline_df=best_df, nb_alpha=estimated_alpha)
        for fam, r in sens_family.items():
            print(f"    {fam}: IRR = {r['irr']:.4f}, p = {r['p_value']:.6f}, "
                  f"deviance/df = {r['deviance_ratio']:.2f}")
        sex_results["sensitivity_family"] = sens_family

        # Sensitivity: Kazoedoshi offset
        print("  [Sensitivity] Kazoedoshi offset...")
        sens_offset = sensitivity_kazoedoshi_offset(sex_df, sex, spline_df=best_df, nb_alpha=estimated_alpha)
        for offset, r in sens_offset.items():
            print(f"    offset={offset}: IRR = {r['irr']:.4f}, p = {r['p_value']:.4f}")
        sex_results["sensitivity_offset"] = sens_offset

        # Sensitivity: Spline df (alpha fixed to primary estimate to isolate spline effect)
        print("  [Sensitivity] Spline degrees of freedom (alpha fixed)...")
        sens_spline = sensitivity_spline_df(sex_df, yaku_ages, nb_alpha=estimated_alpha)
        for df_val, r in sens_spline.items():
            print(f"    df={df_val}: IRR = {r['irr']:.4f}, p = {r['p_value']:.4f}")
        sex_results["sensitivity_spline_df"] = sens_spline

        # Sensitivity: Era (alpha re-estimated per era)
        print("  [Sensitivity] Historical era...")
        sens_era = sensitivity_era(sex_df, yaku_ages, spline_df=best_df)
        for era, r in sens_era.items():
            print(f"    {era}: IRR = {r['irr']:.4f}, p = {r['p_value']:.4f}")
        sex_results["sensitivity_era"] = sens_era

        # Sensitivity: Age range (alpha re-estimated per range)
        print("  [Sensitivity] Age range...")
        df_full_sex = df_long[df_long["Sex"] == sex].copy()
        sens_range = sensitivity_age_range(df_full_sex, yaku_ages, spline_df=best_df)
        for label, r in sens_range.items():
            print(f"    {label}: IRR = {r['irr']:.4f}, p = {r['p_value']:.4f}")
        sex_results["sensitivity_age_range"] = sens_range

        # Sensitivity: Local residual window size
        print("  [Sensitivity] Local residual window...")
        sens_window = sensitivity_residual_window(sex_df, yaku_ages)
        for w, r in sens_window.items():
            print(f"    window=+-{w}: d = {r['cohens_d']:+.4f}, p(perm) = {r['p_permutation']:.4f}")
        sex_results["sensitivity_residual_window"] = sens_window

        results[sex] = sex_results
        print()

    return results


def format_results_table(results: dict) -> str:
    """Format results as a readable summary table."""
    lines = []
    lines.append("=" * 90)
    lines.append("YAKUDOSHI AND MORTALITY: ANALYSIS RESULTS (Negative Binomial, AIC-selected df)")
    lines.append("=" * 90)

    summary = results["data_summary"]
    lines.append(f"\nData: JMD {summary['year_range'][0]}-{summary['year_range'][1]} "
                 f"({summary['n_years']} years), ages {AGE_MIN}-{AGE_MAX}")
    lines.append(f"Total deaths (male, ages {AGE_MIN}-{AGE_MAX}): {summary['total_deaths_male']:,.0f}")
    lines.append(f"Total deaths (female, ages {AGE_MIN}-{AGE_MAX}): {summary['total_deaths_female']:,.0f}")
    lines.append("")

    for sex in ("male", "female"):
        sex_r = results[sex]
        lines.append(f"--- {sex.upper()} ---")
        lines.append(f"  AIC-selected spline df: {sex_r['df_selection']['best_df']}")
        lines.append(f"  Poisson deviance/df_resid: {sex_r['overdispersion_ratio']:.2f}")
        lines.append("")

        # Primary
        for label_key, label in [("primary_hon_yaku", "hon-yaku only"),
                                  ("primary_mae_ato", "with mae/ato-yaku")]:
            r = sex_r[label_key]
            ci = f"({r['irr_ci_low']:.4f}-{r['irr_ci_high']:.4f})"
            lines.append(f"  {label:<25} IRR={r['irr']:.4f} {ci} p={r['p_value']:.4f}")

        # Per-age
        lines.append("  Per-age:")
        for r in sex_r["per_age"]:
            ci = f"({r['irr_ci_low']:.4f}-{r['irr_ci_high']:.4f})"
            lines.append(f"    Age {r['age']}: IRR={r['irr']:.4f} {ci} p={r['p_value']:.4f}")

        # Local residual
        r = sex_r["residual_hon_yaku"]
        lines.append(f"  Local residual: d={r['cohens_d']:+.4f}, p(perm)={r['p_permutation']:.4f}")

        # Poisson vs NB
        lines.append("  Poisson vs NB:")
        for fam, r in sex_r["sensitivity_family"].items():
            ci = f"({r['irr_ci_low']:.4f}-{r['irr_ci_high']:.4f})"
            lines.append(f"    {fam}: IRR={r['irr']:.4f} {ci}, p={r['p_value']:.6f}, "
                         f"deviance/df={r['deviance_ratio']:.2f}")

        # Sensitivity: spline df
        lines.append("  Spline df sensitivity:")
        for df_val, r in sex_r["sensitivity_spline_df"].items():
            ci = f"({r['irr_ci_low']:.4f}-{r['irr_ci_high']:.4f})"
            lines.append(f"    df={df_val}: IRR={r['irr']:.4f} {ci}, p={r['p_value']:.4f}")

        # Sensitivity: offset
        lines.append("  Kazoedoshi offset sensitivity:")
        for offset, r in sex_r["sensitivity_offset"].items():
            ci = f"({r['irr_ci_low']:.4f}-{r['irr_ci_high']:.4f})"
            lines.append(f"    offset={offset}: IRR={r['irr']:.4f} {ci}, p={r['p_value']:.4f}")

        # Sensitivity: era
        lines.append("  Era sensitivity:")
        for era, r in sex_r["sensitivity_era"].items():
            ci = f"({r['irr_ci_low']:.4f}-{r['irr_ci_high']:.4f})"
            lines.append(f"    {era}: IRR={r['irr']:.4f} {ci}, p={r['p_value']:.4f}")

        # Sensitivity: age range
        lines.append("  Age range sensitivity:")
        for label, r in sex_r["sensitivity_age_range"].items():
            ci = f"({r['irr_ci_low']:.4f}-{r['irr_ci_high']:.4f})"
            lines.append(f"    {label}: IRR={r['irr']:.4f} {ci}, p={r['p_value']:.4f}")

        # Sensitivity: residual window
        lines.append("  Residual window sensitivity:")
        for w, r in sex_r["sensitivity_residual_window"].items():
            lines.append(f"    window=+-{w}: d={r['cohens_d']:+.4f}, p(perm)={r['p_permutation']:.4f}")

        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    results = run_full_analysis()
    print("\n")
    print(format_results_table(results))
