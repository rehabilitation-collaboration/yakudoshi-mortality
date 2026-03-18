"""Tests for yakudoshi age definitions."""

from definitions import (
    YAKUDOSHI_KAZOEDOSHI,
    YAKUDOSHI_MANNENREI,
    YAKUDOSHI_WITH_MAE_ATO,
    kazoedoshi_to_mannenrei,
    get_yakudoshi_ages,
    get_yakudoshi_with_mae_ato,
    get_yakudoshi_flag,
    AGE_MIN,
    AGE_MAX,
)


class TestKazoedoshiConversion:
    def test_offset_1(self):
        assert kazoedoshi_to_mannenrei(42, offset=1) == 41
        assert kazoedoshi_to_mannenrei(25, offset=1) == 24

    def test_offset_2(self):
        assert kazoedoshi_to_mannenrei(42, offset=2) == 40
        assert kazoedoshi_to_mannenrei(25, offset=2) == 23


class TestGetYakudoshiAges:
    def test_male_offset_1(self):
        ages = get_yakudoshi_ages("male", offset=1)
        assert ages == [24, 41, 60]

    def test_female_offset_1(self):
        ages = get_yakudoshi_ages("female", offset=1)
        assert ages == [18, 32, 36, 60]

    def test_male_offset_2(self):
        ages = get_yakudoshi_ages("male", offset=2)
        assert ages == [23, 40, 59]

    def test_female_offset_2(self):
        ages = get_yakudoshi_ages("female", offset=2)
        assert ages == [17, 31, 35, 59]

    def test_precomputed_matches(self):
        assert YAKUDOSHI_MANNENREI["male"] == get_yakudoshi_ages("male", 1)
        assert YAKUDOSHI_MANNENREI["female"] == get_yakudoshi_ages("female", 1)


class TestMaeAto:
    def test_male_includes_neighbors(self):
        ages = get_yakudoshi_with_mae_ato("male", offset=1)
        # 24+-1, 41+-1, 60+-1
        assert 23 in ages and 24 in ages and 25 in ages
        assert 40 in ages and 41 in ages and 42 in ages
        assert 59 in ages and 60 in ages and 61 in ages

    def test_female_deduplication(self):
        """Female ages 32 and 36 are close but don't overlap with +-1."""
        ages = get_yakudoshi_with_mae_ato("female", offset=1)
        # 18+-1, 32+-1, 36+-1, 60+-1 -> no overlap
        assert len(ages) == 12  # 4 hon-yaku * 3 - 0 overlaps

    def test_sorted(self):
        for sex in ("male", "female"):
            ages = get_yakudoshi_with_mae_ato(sex, offset=1)
            assert ages == sorted(ages)

    def test_precomputed_matches(self):
        assert YAKUDOSHI_WITH_MAE_ATO["male"] == get_yakudoshi_with_mae_ato("male", 1)
        assert YAKUDOSHI_WITH_MAE_ATO["female"] == get_yakudoshi_with_mae_ato("female", 1)


class TestYakudoshiFlag:
    def test_correct_range(self):
        flag = get_yakudoshi_flag("male", offset=1)
        assert min(flag.keys()) == AGE_MIN
        assert max(flag.keys()) == AGE_MAX

    def test_male_hon_yaku_only(self):
        flag = get_yakudoshi_flag("male", offset=1, include_mae_ato=False)
        assert flag[24] is True
        assert flag[41] is True
        assert flag[60] is True
        assert flag[25] is False
        assert flag[40] is False

    def test_male_with_mae_ato(self):
        flag = get_yakudoshi_flag("male", offset=1, include_mae_ato=True)
        assert flag[23] is True  # mae-yaku of 24
        assert flag[24] is True
        assert flag[25] is True  # ato-yaku of 24
        assert flag[26] is False
