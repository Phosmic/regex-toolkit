import pytest

from regex_toolkit.enums import RegexFlavor


def test_regex_flavor_enum_is_int():
    assert isinstance(RegexFlavor.RE, int)
    assert RegexFlavor.RE == 1
    assert RegexFlavor(1) == RegexFlavor.RE
    assert isinstance(RegexFlavor.RE2, int)
    assert RegexFlavor.RE2 == 2
    assert RegexFlavor(2) == RegexFlavor.RE2


def test_invalid_regex_flavor_raises_value_error():
    with pytest.raises(ValueError):
        RegexFlavor(0)

    with pytest.raises(ValueError):
        RegexFlavor(3)
