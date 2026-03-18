"""
Publication-quality figures for the yakudoshi mortality paper.

Figure 1: Age-specific mortality curves with yakudoshi ages highlighted.
Figure 2: Local residual distributions (yakudoshi vs non-yakudoshi).
Figure 3: Forest plot of IRR per yakudoshi age + sensitivity analyses.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

from data_loader import load_mortality_long, filter_analysis_range
from definitions import (
    AGE_MIN, AGE_MAX, NEIGHBOR_WINDOW,
    YAKUDOSHI_MANNENREI, YAKUDOSHI_KAZOEDOSHI,
    get_yakudoshi_ages,
)
from analysis import (
    fit_regression_model, fit_per_age,
    compute_local_residuals, evaluate_local_residuals,
    sensitivity_spline_df, sensitivity_era,
    select_spline_df, estimate_nb_alpha,
)

# Publication style settings
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 9,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

OUTPUT_DIR = "output"
SEX_LABELS = {"male": "Male", "female": "Female"}
SEX_COLORS = {"male": "#2171B5", "female": "#CB181D"}
YAKU_COLOR = "#E31A1C"
NON_YAKU_COLOR = "#969696"


def figure1_mortality_curves(df: pd.DataFrame):
    """Age-specific mortality curves with yakudoshi ages highlighted.

    Shows 78 years of age-mortality curves (thin lines) with median (thick line)
    and yakudoshi ages marked with vertical bands.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)

    for ax, sex in zip(axes, ("male", "female")):
        sex_df = df[df["Sex"] == sex]
        yaku_ages = YAKUDOSHI_MANNENREI[sex]
        kazoedoshi = YAKUDOSHI_KAZOEDOSHI[sex]

        # Plot each year as a thin line
        for year in sex_df["Year"].unique():
            year_df = sex_df[sex_df["Year"] == year].sort_values("Age")
            ax.plot(year_df["Age"], year_df["Mx"],
                    color=SEX_COLORS[sex], alpha=0.06, linewidth=0.3)

        # Median line across years
        median_mx = sex_df.groupby("Age")["Mx"].median()
        ax.plot(median_mx.index, median_mx.values,
                color=SEX_COLORS[sex], linewidth=1.8, label="Median (1947-2024)")

        # Yakudoshi vertical bands
        for yaku_age, kazoe in zip(yaku_ages, kazoedoshi):
            ax.axvspan(yaku_age - 0.4, yaku_age + 0.4,
                       alpha=0.15, color=YAKU_COLOR, zorder=0)
            # Label with kazoedoshi age
            y_pos = median_mx.loc[yaku_age] if yaku_age in median_mx.index else 0.01
            ax.annotate(f"{kazoe}\n(kazoe)",
                        xy=(yaku_age, y_pos),
                        xytext=(0, 25), textcoords="offset points",
                        fontsize=7, ha="center", color=YAKU_COLOR,
                        arrowprops=dict(arrowstyle="-", color=YAKU_COLOR,
                                        linewidth=0.5))

        ax.set_yscale("log")
        ax.set_xlabel("Age (mannenrei)")
        ax.set_title(f"{SEX_LABELS[sex]}")
        ax.set_xlim(AGE_MIN, AGE_MAX)

        # Custom legend
        legend_elements = [
            Line2D([0], [0], color=SEX_COLORS[sex], linewidth=1.8, label="Median"),
            Line2D([0], [0], color=SEX_COLORS[sex], alpha=0.3, linewidth=1, label="Individual years"),
            plt.Rectangle((0, 0), 1, 1, fc=YAKU_COLOR, alpha=0.15, label="Yakudoshi age"),
        ]
        ax.legend(handles=legend_elements, loc="upper left", framealpha=0.9)

    axes[0].set_ylabel("Mortality rate (Mx, log scale)")

    fig.suptitle("Age-Specific Mortality Rates in Japan, 1947-2024",
                 fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/figure1_mortality_curves.png")
    fig.savefig(f"{OUTPUT_DIR}/figure1_mortality_curves.pdf")
    plt.close(fig)
    print("Figure 1 saved.")


def figure2_residual_distributions(df: pd.DataFrame):
    """Local residual distributions: yakudoshi vs non-yakudoshi ages.

    Box + strip plot showing residual distributions across 78 years.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)

    for ax, sex in zip(axes, ("male", "female")):
        sex_df = df[df["Sex"] == sex]
        yaku_ages = set(YAKUDOSHI_MANNENREI[sex])

        yaku_residuals = []
        non_yaku_residuals = []

        for year in sex_df["Year"].unique():
            year_df = sex_df[sex_df["Year"] == year].sort_values("Age").reset_index(drop=True)
            year_df = year_df.dropna(subset=["Mx"])
            if len(year_df) < 10:
                continue

            resid = compute_local_residuals(year_df["Mx"], year_df["Age"])
            for i, val in enumerate(resid):
                if np.isnan(val):
                    continue
                age = year_df.iloc[i]["Age"]
                if age in yaku_ages:
                    yaku_residuals.append(val)
                else:
                    non_yaku_residuals.append(val)

        # Box plot
        bp = ax.boxplot(
            [non_yaku_residuals, yaku_residuals],
            tick_labels=["Non-yakudoshi", "Yakudoshi"],
            widths=0.5,
            patch_artist=True,
            showfliers=False,
            medianprops=dict(color="black", linewidth=1.5),
        )
        bp["boxes"][0].set_facecolor(NON_YAKU_COLOR)
        bp["boxes"][0].set_alpha(0.4)
        bp["boxes"][1].set_facecolor(YAKU_COLOR)
        bp["boxes"][1].set_alpha(0.4)

        # Jittered strip overlay for yakudoshi (small n, visible points)
        rng = np.random.default_rng(42)
        jitter = rng.uniform(-0.08, 0.08, size=len(yaku_residuals))
        ax.scatter(
            np.full(len(yaku_residuals), 2) + jitter,
            yaku_residuals,
            color=YAKU_COLOR, alpha=0.15, s=8, zorder=3,
        )

        ax.axhline(0, color="black", linewidth=0.5, linestyle="--", alpha=0.5)
        ax.set_ylabel("Local residual (log Mx)" if sex == "male" else "")
        ax.set_title(f"{SEX_LABELS[sex]}")

        # Annotate statistics
        test_result = evaluate_local_residuals(
            sex_df, list(yaku_ages), NEIGHBOR_WINDOW
        )
        stats_text = (
            f"Mean diff: {test_result['mean_yaku_residual']:+.4f}\n"
            f"p(perm) = {test_result['p_permutation']:.3f}\n"
            f"Cohen's d = {test_result['cohens_d']:+.3f}"
        )
        ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
                fontsize=7, va="top", ha="right",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor="gray", alpha=0.8))

    fig.suptitle("Local Residuals at Yakudoshi vs Non-Yakudoshi Ages",
                 fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/figure2_residual_distributions.png")
    fig.savefig(f"{OUTPUT_DIR}/figure2_residual_distributions.pdf")
    plt.close(fig)
    print("Figure 2 saved.")


def figure3_forest_plot(df: pd.DataFrame):
    """Forest plot of IRR per yakudoshi age and sensitivity analyses."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 7), sharey=False)

    for ax, sex in zip(axes, ("male", "female")):
        sex_df = df[df["Sex"] == sex].copy()
        yaku_ages = YAKUDOSHI_MANNENREI[sex]

        # Use AIC-selected spline df and estimated alpha (consistent with analysis.py)
        df_selection = select_spline_df(sex_df, yaku_ages)
        best_df = df_selection["best_df"]
        estimated_alpha = estimate_nb_alpha(sex_df, best_df)

        rows = []  # (label, irr, ci_low, ci_high, is_header)

        # Per-age results (NB regression)
        per_age_results = fit_per_age(sex_df, yaku_ages, spline_df=best_df, nb_alpha=estimated_alpha)
        rows.append(("Per-age analysis (NB)", None, None, None, True))
        for r in per_age_results:
            kazoe = r["age"] + 1  # approximate kazoedoshi
            rows.append((
                f"  Age {r['age']} (kazoe {kazoe})",
                r["irr"], r["irr_ci_low"], r["irr_ci_high"], False
            ))

        # Overall (NB)
        overall = fit_regression_model(sex_df, yaku_ages, spline_df=best_df, nb_alpha=estimated_alpha)
        rows.append(("", None, None, None, True))
        rows.append(("Overall (hon-yaku, NB)", None, None, None, True))
        rows.append((
            f"  All yakudoshi ages",
            overall["irr"], overall["irr_ci_low"], overall["irr_ci_high"], False
        ))

        # Sensitivity: spline df (alpha fixed to isolate spline effect)
        rows.append(("", None, None, None, True))
        rows.append(("Sensitivity: spline df", None, None, None, True))
        sens_spline = sensitivity_spline_df(sex_df, yaku_ages, nb_alpha=estimated_alpha)
        for df_val, r in sens_spline.items():
            rows.append((
                f"  df = {df_val}",
                r["irr"], r["irr_ci_low"], r["irr_ci_high"], False
            ))

        # Sensitivity: era (alpha re-estimated per era)
        rows.append(("", None, None, None, True))
        rows.append(("Sensitivity: era", None, None, None, True))
        sens_era = sensitivity_era(sex_df, yaku_ages, spline_df=best_df)
        for era, r in sens_era.items():
            label = era.split("(")[0].strip().capitalize()
            rows.append((
                f"  {label}",
                r["irr"], r["irr_ci_low"], r["irr_ci_high"], False
            ))

        # Sensitivity: kazoedoshi offset=2
        offset2_ages = get_yakudoshi_ages(sex, offset=2)
        r_offset2 = fit_regression_model(sex_df, offset2_ages, spline_df=best_df, nb_alpha=estimated_alpha)
        rows.append(("", None, None, None, True))
        rows.append(("Sensitivity: kazoe offset", None, None, None, True))
        rows.append((
            f"  offset = 1 (primary)",
            overall["irr"], overall["irr_ci_low"], overall["irr_ci_high"], False
        ))
        rows.append((
            f"  offset = 2",
            r_offset2["irr"], r_offset2["irr_ci_low"], r_offset2["irr_ci_high"], False
        ))

        # Draw forest plot
        y_positions = list(range(len(rows) - 1, -1, -1))

        for y, (label, irr, ci_low, ci_high, is_header) in zip(y_positions, rows):
            if is_header:
                ax.text(-0.02, y, label, transform=ax.get_yaxis_transform(),
                        fontsize=8, fontweight="bold", va="center", ha="right")
            elif irr is not None:
                # Point estimate
                ax.plot(irr, y, "D", color=SEX_COLORS[sex], markersize=5, zorder=3)
                # CI line
                ax.plot([ci_low, ci_high], [y, y],
                        color=SEX_COLORS[sex], linewidth=1.5, zorder=2)
                # Label
                ax.text(-0.02, y, label, transform=ax.get_yaxis_transform(),
                        fontsize=7, va="center", ha="right")
                # IRR text on right
                ax.text(1.02, y, f"{irr:.3f} ({ci_low:.3f}-{ci_high:.3f})",
                        transform=ax.get_yaxis_transform(),
                        fontsize=6.5, va="center", ha="left")

        # Reference line at IRR=1
        ax.axvline(1.0, color="black", linewidth=0.8, linestyle="--", alpha=0.6)

        ax.set_ylim(-1, len(rows))
        ax.set_yticks([])
        ax.set_xlabel("Incidence Rate Ratio (IRR)")
        ax.set_title(f"{SEX_LABELS[sex]}", fontweight="bold")

        # Set reasonable x-limits
        all_irrs = [r[1] for r in rows if r[1] is not None]
        all_ci_low = [r[2] for r in rows if r[2] is not None]
        all_ci_high = [r[3] for r in rows if r[3] is not None]
        x_min = min(all_ci_low) - 0.02
        x_max = max(all_ci_high) + 0.02
        ax.set_xlim(x_min, x_max)

    fig.suptitle("Incidence Rate Ratios for Yakudoshi Ages\n(Negative Binomial Regression)",
                 fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.subplots_adjust(left=0.25, right=0.82)
    fig.savefig(f"{OUTPUT_DIR}/figure3_forest_plot.png")
    fig.savefig(f"{OUTPUT_DIR}/figure3_forest_plot.pdf")
    plt.close(fig)
    print("Figure 3 saved.")


def generate_all_figures():
    """Generate all publication figures."""
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Loading data...")
    df_long = load_mortality_long()
    df = filter_analysis_range(df_long, AGE_MIN, AGE_MAX)

    print("Generating Figure 1: Mortality curves...")
    figure1_mortality_curves(df)

    print("Generating Figure 2: Residual distributions...")
    figure2_residual_distributions(df)

    print("Generating Figure 3: Forest plot...")
    figure3_forest_plot(df)

    print("\nAll figures saved to output/")


if __name__ == "__main__":
    generate_all_figures()
