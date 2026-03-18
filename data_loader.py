"""
JMD (Japanese Mortality Database) data loader.

Data source: National Institute of Population and Social Security Research (IPSS)
URL: https://www.ipss.go.jp/p-toukei/JMD/index.asp
Format: Space-delimited text, 1947-2024, ages 0-110+
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

JMD_FILES = {
    "mx": DATA_DIR / "Mx_1x1.txt",
    "deaths": DATA_DIR / "Deaths_1x1.txt",
    "exposures": DATA_DIR / "Exposures_1x1.txt",
}

# JMD file format constants
SKIP_ROWS = 2  # 1 metadata line + 1 blank line
NA_VALUE = "."
MAX_NUMERIC_AGE = 110  # "110+" is the open-ended interval


def load_jmd_file(file_type: str) -> pd.DataFrame:
    """Load a single JMD data file.

    Args:
        file_type: One of "mx", "deaths", "exposures".

    Returns:
        DataFrame with columns: Year (int), Age (int), Female, Male, Total (float).
        The "110+" age group is excluded (not usable for age-specific analysis).
    """
    filepath = JMD_FILES[file_type]

    df = pd.read_csv(
        filepath,
        sep=r"\s+",
        skiprows=SKIP_ROWS,
        na_values=NA_VALUE,
        engine="python",
    )

    # Drop "110+" rows (Age column is string due to "110+")
    df = df[df["Age"] != "110+"].copy()
    df["Age"] = df["Age"].astype(int)
    df["Year"] = df["Year"].astype(int)

    # Ensure numeric columns
    for col in ("Female", "Male", "Total"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def load_all_jmd() -> dict[str, pd.DataFrame]:
    """Load all three JMD files.

    Returns:
        Dict with keys "mx", "deaths", "exposures", each containing a DataFrame.
    """
    return {ft: load_jmd_file(ft) for ft in JMD_FILES}


def load_mortality_long() -> pd.DataFrame:
    """Load JMD data in long format suitable for regression analysis.

    Returns:
        DataFrame with columns:
        Year, Age, Sex ("male"/"female"), Deaths, Exposures, Mx
    """
    deaths_df = load_jmd_file("deaths")
    exposures_df = load_jmd_file("exposures")
    mx_df = load_jmd_file("mx")

    # Verify row alignment across files
    assert (deaths_df["Year"].values == exposures_df["Year"].values).all(), \
        "Year mismatch between Deaths and Exposures files"
    assert (deaths_df["Age"].values == exposures_df["Age"].values).all(), \
        "Age mismatch between Deaths and Exposures files"
    assert (deaths_df["Year"].values == mx_df["Year"].values).all(), \
        "Year mismatch between Deaths and Mx files"
    assert (deaths_df["Age"].values == mx_df["Age"].values).all(), \
        "Age mismatch between Deaths and Mx files"

    records = []
    for sex_col, sex_label in [("Male", "male"), ("Female", "female")]:
        df = pd.DataFrame({
            "Year": deaths_df["Year"].values,
            "Age": deaths_df["Age"].values,
            "Sex": sex_label,
            "Deaths": deaths_df[sex_col].values,
            "Exposures": exposures_df[sex_col].values,
            "Mx": mx_df[sex_col].values,
        })
        records.append(df)

    long_df = pd.concat(records, ignore_index=True)

    # Compute Mx from Deaths/Exposures where Mx is missing
    mask = long_df["Mx"].isna() & long_df["Exposures"].gt(0)
    long_df.loc[mask, "Mx"] = long_df.loc[mask, "Deaths"] / long_df.loc[mask, "Exposures"]

    return long_df


def filter_analysis_range(df: pd.DataFrame, age_min: int, age_max: int,
                          year_min: int | None = None, year_max: int | None = None) -> pd.DataFrame:
    """Filter DataFrame to analysis age and year range.

    Args:
        df: DataFrame with Age and Year columns.
        age_min: Minimum age (inclusive).
        age_max: Maximum age (inclusive).
        year_min: Minimum year (inclusive). None = no filter.
        year_max: Maximum year (inclusive). None = no filter.

    Returns:
        Filtered DataFrame.
    """
    mask = (df["Age"] >= age_min) & (df["Age"] <= age_max)
    if year_min is not None:
        mask &= df["Year"] >= year_min
    if year_max is not None:
        mask &= df["Year"] <= year_max
    return df[mask].copy()


def get_data_summary(df: pd.DataFrame) -> dict:
    """Get summary statistics for the dataset.

    Args:
        df: Long-format DataFrame from load_mortality_long().

    Returns:
        Dict with summary statistics.
    """
    return {
        "year_range": (int(df["Year"].min()), int(df["Year"].max())),
        "n_years": int(df["Year"].nunique()),
        "age_range": (int(df["Age"].min()), int(df["Age"].max())),
        "total_deaths_male": float(df.loc[df["Sex"] == "male", "Deaths"].sum()),
        "total_deaths_female": float(df.loc[df["Sex"] == "female", "Deaths"].sum()),
        "total_person_years_male": float(df.loc[df["Sex"] == "male", "Exposures"].sum()),
        "total_person_years_female": float(df.loc[df["Sex"] == "female", "Exposures"].sum()),
        "n_missing_mx": int(df["Mx"].isna().sum()),
    }
