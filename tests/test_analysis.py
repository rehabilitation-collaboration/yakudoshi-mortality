"""Tests for the statistical analysis module."""

import numpy as np
import pandas as pd
import pytest

from analysis import (
    compute_local_residuals,
    estimate_nb_alpha,
    fit_regression_model,
    evaluate_local_residuals,
    sensitivity_residual_window,
)
from definitions import NEIGHBOR_WINDOW


class TestComputeLocalResiduals:
    """Tests for compute_local_residuals."""

    def test_perfectly_smooth_curve_gives_zero_residuals(self):
        """A perfectly exponential curve should have zero residuals."""
        ages = pd.Series(range(20, 31))
        # Exponential: log(Mx) is linear in age -> residuals should be ~0
        mx = pd.Series(np.exp(0.1 * ages.values))
        resid = compute_local_residuals(mx, ages, window=3)

        # Interior ages (where full window is available) should be near zero
        interior = resid.iloc[3:-3].dropna()
        assert len(interior) > 0
        assert np.allclose(interior.values, 0, atol=1e-10)

    def test_spike_produces_positive_residual(self):
        """An age with elevated mortality should have a positive residual."""
        ages = pd.Series(range(20, 31))
        mx_vals = np.exp(0.1 * ages.values).astype(float)
        # Add a spike at age 25 (index 5)
        mx_vals[5] *= 2.0
        mx = pd.Series(mx_vals)
        resid = compute_local_residuals(mx, ages, window=3)

        assert resid.iloc[5] > 0

    def test_dip_produces_negative_residual(self):
        """An age with reduced mortality should have a negative residual."""
        ages = pd.Series(range(20, 31))
        mx_vals = np.exp(0.1 * ages.values).astype(float)
        # Halve mortality at age 25
        mx_vals[5] *= 0.5
        mx = pd.Series(mx_vals)
        resid = compute_local_residuals(mx, ages, window=3)

        assert resid.iloc[5] < 0

    def test_boundary_ages_have_nan(self):
        """Ages at the very boundary without enough neighbors should have NaN."""
        ages = pd.Series([15])
        mx = pd.Series([0.001])
        resid = compute_local_residuals(mx, ages, window=3)
        assert np.isnan(resid.iloc[0])

    def test_window_parameter_affects_neighbors(self):
        """Different window sizes should use different neighbor sets."""
        # Use a non-linear curve so that different windows give different means
        ages = pd.Series(range(20, 51))
        mx_vals = np.exp(0.01 * (ages.values - 35) ** 2).astype(float)
        mx_vals[15] *= 1.5  # spike at age 35
        mx = pd.Series(mx_vals)

        resid_w2 = compute_local_residuals(mx, ages, window=2)
        resid_w5 = compute_local_residuals(mx, ages, window=5)

        # Both should be positive at the spike, but magnitudes differ
        assert resid_w2.iloc[15] > 0
        assert resid_w5.iloc[15] > 0
        assert not np.isclose(resid_w2.iloc[15], resid_w5.iloc[15])

    def test_output_same_length_as_input(self):
        """Output should have the same length and index as input."""
        ages = pd.Series(range(20, 50), index=range(100, 130))
        mx = pd.Series(np.exp(0.05 * ages.values), index=range(100, 130))
        resid = compute_local_residuals(mx, ages, window=3)

        assert len(resid) == len(mx)
        assert (resid.index == mx.index).all()


class TestFitRegressionModel:
    """Tests for fit_regression_model with real JMD data."""

    @pytest.fixture(scope="class")
    def male_df(self):
        """Load real male data for ages 15-80."""
        from data_loader import load_mortality_long, filter_analysis_range
        from definitions import AGE_MIN, AGE_MAX
        df = load_mortality_long()
        df = filter_analysis_range(df, AGE_MIN, AGE_MAX)
        return df[df["Sex"] == "male"].copy()

    def test_returns_expected_keys(self, male_df):
        """Result dict should contain all expected keys."""
        result = fit_regression_model(male_df, [24, 41, 60], spline_df=5, family="poisson")
        expected_keys = {
            "coefficient", "se", "irr", "irr_ci_low", "irr_ci_high",
            "p_value", "aic", "deviance", "df_resid", "deviance_ratio",
            "nb_alpha", "n_obs", "spline_df", "family", "model_result",
        }
        assert expected_keys == set(result.keys())

    def test_irr_is_exp_of_coefficient(self, male_df):
        """IRR should equal exp(coefficient)."""
        result = fit_regression_model(male_df, [24, 41, 60], spline_df=5, family="poisson")
        assert np.isclose(result["irr"], np.exp(result["coefficient"]))

    def test_ci_contains_irr(self, male_df):
        """95% CI should contain the point estimate."""
        result = fit_regression_model(male_df, [24, 41, 60], spline_df=5, family="poisson")
        assert result["irr_ci_low"] <= result["irr"] <= result["irr_ci_high"]

    def test_poisson_has_no_alpha(self, male_df):
        """Poisson model should have nb_alpha=None."""
        result = fit_regression_model(male_df, [24, 41, 60], spline_df=5, family="poisson")
        assert result["nb_alpha"] is None
        assert result["family"] == "poisson"

    def test_nb_has_alpha(self, male_df):
        """NB model should have nb_alpha set."""
        result = fit_regression_model(male_df, [24, 41, 60], spline_df=5, family="nb")
        assert result["nb_alpha"] is not None
        assert result["nb_alpha"] > 0
        assert result["family"] == "nb"

    def test_poisson_overdispersion(self, male_df):
        """Poisson model on this data should show overdispersion (deviance/df >> 1)."""
        result = fit_regression_model(male_df, [24, 41, 60], spline_df=5, family="poisson")
        assert result["deviance_ratio"] > 10

    def test_nb_appropriate_fit(self, male_df):
        """NB model should have deviance/df near 1.0."""
        result = fit_regression_model(male_df, [24, 41, 60], spline_df=5, family="nb")
        assert 0.1 < result["deviance_ratio"] < 5.0


class TestEstimateNbAlpha:
    """Tests for estimate_nb_alpha."""

    @pytest.fixture(scope="class")
    def male_df(self):
        from data_loader import load_mortality_long, filter_analysis_range
        from definitions import AGE_MIN, AGE_MAX
        df = load_mortality_long()
        df = filter_analysis_range(df, AGE_MIN, AGE_MAX)
        return df[df["Sex"] == "male"].copy()

    def test_alpha_is_positive(self, male_df):
        """Estimated alpha should be positive."""
        alpha = estimate_nb_alpha(male_df, spline_df=5)
        assert alpha > 0

    def test_alpha_is_reasonable(self, male_df):
        """Alpha should be in a reasonable range (not extreme)."""
        alpha = estimate_nb_alpha(male_df, spline_df=5)
        assert 1e-4 < alpha < 10


class TestCohensD:
    """Test Cohen's d calculation in evaluate_local_residuals."""

    @pytest.fixture(scope="class")
    def male_df(self):
        from data_loader import load_mortality_long, filter_analysis_range
        from definitions import AGE_MIN, AGE_MAX
        df = load_mortality_long()
        df = filter_analysis_range(df, AGE_MIN, AGE_MAX)
        return df[df["Sex"] == "male"].copy()

    def test_cohens_d_is_small(self, male_df):
        """Cohen's d for yakudoshi should be small (d < 0.2)."""
        result = evaluate_local_residuals(male_df, [24, 41, 60])
        assert abs(result["cohens_d"]) < 0.2

    def test_observation_counts_positive(self, male_df):
        """Both groups should have observations."""
        result = evaluate_local_residuals(male_df, [24, 41, 60])
        assert result["n_yakudoshi_obs"] > 0
        assert result["n_non_yakudoshi_obs"] > 0
        assert result["n_non_yakudoshi_obs"] > result["n_yakudoshi_obs"]


class TestSensitivityResidualWindow:
    """Tests for sensitivity_residual_window."""

    @pytest.fixture(scope="class")
    def male_df(self):
        from data_loader import load_mortality_long, filter_analysis_range
        from definitions import AGE_MIN, AGE_MAX
        df = load_mortality_long()
        df = filter_analysis_range(df, AGE_MIN, AGE_MAX)
        return df[df["Sex"] == "male"].copy()

    def test_returns_all_windows(self, male_df):
        """Should return results for all requested window sizes."""
        result = sensitivity_residual_window(male_df, [24, 41, 60], windows=(2, 3, 4, 5))
        assert set(result.keys()) == {2, 3, 4, 5}

    def test_each_window_has_cohens_d(self, male_df):
        """Each window result should contain Cohen's d."""
        result = sensitivity_residual_window(male_df, [24, 41, 60], windows=(2, 3))
        for w, r in result.items():
            assert "cohens_d" in r
            assert "p_permutation" in r
