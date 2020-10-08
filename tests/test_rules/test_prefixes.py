import pytest

from carbonpy.rules.prefixes import to_place_values, get_prefix

numbers = [14, 23, 41, 52, 363]
prefixes = ["tetradec", "tricos", "hentetracont", "dopentacont", "trihexacontatrict"]


def test_to_place_values():
    assert list(to_place_values(100)) == [0, 0, 100]
    assert list(to_place_values(123)) == [3, 20, 100]
    assert list(to_place_values(1043)) == [3, 40, 0, 1000]


@pytest.mark.parametrize(argnames='number,prefix', argvalues=zip(numbers, prefixes))
def test_get_prefix(number, prefix):
    assert get_prefix(number, parent=True) == prefix
    assert get_prefix(number, parent=False) == f"{prefix}a"
