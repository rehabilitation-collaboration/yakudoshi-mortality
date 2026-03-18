"""Tests for JMD data loader."""

import numpy as np
import pandas as pd

from data_loader import (
    load_jmd_file,
    load_mortality_long,
    filter_analysis_range,
    get_data_summary,
)


class TestLoadJmdFile:
    def test_mx_loads(self):
        df = load_jmd_file("mx")
        assert isinstance(df, pd.DataFrame)
        assert set(df.columns) == {"Year", "Age", "Female", "Male", "Total"}

    def test_no_110_plus(self):
        """110+ age group should be excluded."""
        df = load_jmd_file("mx")
        assert df["Age"].max() <= 110
        assert "110+" not in df["Age"].values

    def test_year_range(self):
        df = load_jmd_file("mx")
        assert df["Year"].min() == 1947
        assert df["Year"].max() == 2024

    def test_age_range(self):
        df = load_jmd_file("mx")
        assert df["Age"].min() == 0
        assert df["Age"].max() == 109  # 110+ excluded, so max is 109

    def test_deaths_no_missing(self):
        """Deaths file should have no missing values."""
        df = load_jmd_file("deaths")
        assert df["Female"].isna().sum() == 0
        assert df["Male"].isna().sum() == 0

    def test_exposures_no_missing(self):
        """Exposures file should have no missing values."""
        df = load_jmd_file("exposures")
        assert df["Female"].isna().sum() == 0
        assert df["Male"].isna().sum() == 0

    def test_row_count(self):
        """Each year has 110 ages (0-109), 78 years = 8580 rows."""
        df = load_jmd_file("mx")
        n_years = df["Year"].nunique()
        n_ages = df["Age"].nunique()
        assert n_years == 78
        assert n_ages == 110  # 0-109
        assert len(df) == n_years * n_ages


class TestLoadMortalityLong:
    def test_columns(self):
        df = load_mortality_long()
        assert set(df.columns) == {"Year", "Age", "Sex", "Deaths", "Exposures", "Mx"}

    def test_sex_values(self):
        df = load_mortality_long()
        assert set(df["Sex"].unique()) == {"male", "female"}

    def test_double_row_count(self):
        """Long format should have 2x rows (male + female)."""
        df_wide = load_jmd_file("mx")
        df_long = load_mortality_long()
        assert len(df_long) == 2 * len(df_wide)


class TestMxConsistency:
    def test_mx_equals_deaths_over_exposures(self):
        """Mx should approximately equal Deaths/Exposures."""
        df = load_mortality_long()
        # Filter to rows where all values are present
        valid = df.dropna(subset=["Mx", "Deaths", "Exposures"])
        valid = valid[valid["Exposures"] > 0]

        computed_mx = valid["Deaths"] / valid["Exposures"]
        diff = np.abs(valid["Mx"] - computed_mx)

        # Most values match closely; a few high-age cells have larger
        # rounding differences due to small denominators
        assert (diff < 0.01).mean() > 0.998, f"Too many large diffs"
        assert diff.median() < 1e-5, f"Median diff too large: {diff.median()}"


class TestSanityChecks:
    def test_mortality_increases_with_age(self):
        """After age 30, mortality should generally increase with age."""
        df = load_mortality_long()
        for sex in ("male", "female"):
            sex_df = df[(df["Sex"] == sex) & (df["Age"] >= 30) & (df["Age"] <= 80)]
            mean_by_age = sex_df.groupby("Age")["Mx"].mean()
            # Spearman correlation with age should be strongly positive
            from scipy.stats import spearmanr
            corr, _ = spearmanr(mean_by_age.index, mean_by_age.values)
            assert corr > 0.95, f"{sex} age-mortality correlation: {corr}"

    def test_male_higher_than_female(self):
        """Male mortality should generally be higher than female."""
        df = load_mortality_long()
        df_adult = df[(df["Age"] >= 20) & (df["Age"] <= 80)]
        male_mean = df_adult[df_adult["Sex"] == "male"]["Mx"].mean()
        female_mean = df_adult[df_adult["Sex"] == "female"]["Mx"].mean()
        assert male_mean > female_mean

    def test_j_curve_pattern(self):
        """Infant mortality should be higher than child mortality (J-curve)."""
        df = load_mortality_long()
        recent = df[df["Year"] >= 2000]
        for sex in ("male", "female"):
            sex_df = recent[recent["Sex"] == sex]
            infant_mx = sex_df[sex_df["Age"] == 0]["Mx"].mean()
            child_mx = sex_df[(sex_df["Age"] >= 5) & (sex_df["Age"] <= 10)]["Mx"].mean()
            assert infant_mx > child_mx, f"{sex}: infant {infant_mx} <= child {child_mx}"


class TestFilterAnalysisRange:
    def test_age_filter(self):
        df = load_mortality_long()
        filtered = filter_analysis_range(df, 15, 80)
        assert filtered["Age"].min() >= 15
        assert filtered["Age"].max() <= 80

    def test_year_filter(self):
        df = load_mortality_long()
        filtered = filter_analysis_range(df, 15, 80, year_min=2000, year_max=2020)
        assert filtered["Year"].min() >= 2000
        assert filtered["Year"].max() <= 2020


class TestGetDataSummary:
    def test_summary_keys(self):
        df = load_mortality_long()
        summary = get_data_summary(df)
        assert "year_range" in summary
        assert "n_years" in summary
        assert "total_deaths_male" in summary
        assert "n_missing_mx" in summary

    def test_summary_values(self):
        df = load_mortality_long()
        summary = get_data_summary(df)
        assert summary["n_years"] == 78
        assert summary["year_range"] == (1947, 2024)
        assert summary["total_deaths_male"] > 0
        assert summary["total_deaths_female"] > 0
