"""
Yakudoshi (unlucky years) age definitions.

Traditional yakudoshi ages are defined in kazoedoshi (counting age).
JMD data uses mannenrei (Western/full age). This module provides
both representations and utilities for conversion.
"""

# Yakudoshi ages in kazoedoshi (traditional counting age)
# Born = age 1, +1 every New Year's Day
YAKUDOSHI_KAZOEDOSHI = {
    "male": [25, 42, 61],
    "female": [19, 33, 37, 61],
}

# Taiyaku (great unlucky year) in kazoedoshi
TAIYAKU_KAZOEDOSHI = {
    "male": 42,
    "female": 33,
}

# Analysis age range (exclude infants and very old)
AGE_MIN = 15
AGE_MAX = 80

# Local residual method: neighbor window size
NEIGHBOR_WINDOW = 3


def kazoedoshi_to_mannenrei(kazoedoshi_age: int, offset: int = 1) -> int:
    """Convert kazoedoshi to mannenrei.

    The exact mapping depends on birth date relative to New Year:
    - Born Jan-Dec: kazoedoshi = mannenrei + 1 (after birthday)
    - Born late in year: kazoedoshi = mannenrei + 2 (before birthday in new year)

    Args:
        kazoedoshi_age: Age in kazoedoshi system.
        offset: 1 (primary analysis) or 2 (sensitivity analysis).

    Returns:
        Age in mannenrei (Western age).
    """
    return kazoedoshi_age - offset


def get_yakudoshi_ages(sex: str, offset: int = 1) -> list[int]:
    """Get hon-yaku (main unlucky year) ages in mannenrei.

    Args:
        sex: "male" or "female".
        offset: 1 for primary analysis, 2 for sensitivity analysis.

    Returns:
        Sorted list of yakudoshi ages in mannenrei.
    """
    return sorted(
        kazoedoshi_to_mannenrei(a, offset) for a in YAKUDOSHI_KAZOEDOSHI[sex]
    )


def get_yakudoshi_with_mae_ato(sex: str, offset: int = 1) -> list[int]:
    """Get yakudoshi ages including mae-yaku and ato-yaku (+-1 year).

    Args:
        sex: "male" or "female".
        offset: 1 for primary analysis, 2 for sensitivity analysis.

    Returns:
        Sorted, deduplicated list of ages in mannenrei.
    """
    hon_yaku = get_yakudoshi_ages(sex, offset)
    all_ages = set()
    for age in hon_yaku:
        all_ages.update([age - 1, age, age + 1])
    return sorted(all_ages)


def get_yakudoshi_flag(sex: str, offset: int = 1, include_mae_ato: bool = False) -> dict[int, bool]:
    """Get a dict mapping each age in AGE_MIN..AGE_MAX to yakudoshi status.

    Args:
        sex: "male" or "female".
        offset: 1 for primary analysis, 2 for sensitivity analysis.
        include_mae_ato: If True, include mae-yaku and ato-yaku.

    Returns:
        Dict of {age: is_yakudoshi}.
    """
    if include_mae_ato:
        yaku_ages = set(get_yakudoshi_with_mae_ato(sex, offset))
    else:
        yaku_ages = set(get_yakudoshi_ages(sex, offset))

    return {age: age in yaku_ages for age in range(AGE_MIN, AGE_MAX + 1)}


# Pre-computed age lists for convenience (primary analysis, offset=1)
YAKUDOSHI_MANNENREI = {
    sex: get_yakudoshi_ages(sex, offset=1) for sex in ("male", "female")
}
# male: [24, 41, 60], female: [18, 32, 36, 60]

YAKUDOSHI_WITH_MAE_ATO = {
    sex: get_yakudoshi_with_mae_ato(sex, offset=1) for sex in ("male", "female")
}
