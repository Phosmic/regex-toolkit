import pytest

from regex_toolkit.enums import RegexFlavor


def test_regex_flavor_enum_has_expected_members():
    assert len(RegexFlavor) == 2
    assert len(set(RegexFlavor)) == len(RegexFlavor)

    assert RegexFlavor.RE.name == "RE"
    assert RegexFlavor.RE.value == RegexFlavor.RE == RegexFlavor(1) == 1
    assert RegexFlavor(1) is RegexFlavor.RE

    assert RegexFlavor.RE2.name == "RE2"
    assert RegexFlavor.RE2 == RegexFlavor.RE2.value == RegexFlavor(2) == 2
    assert RegexFlavor(2) is RegexFlavor.RE2


@pytest.mark.parametrize("invalid_flavor", (0, 3))
def test_invalid_regex_flavor_raises_value_error(invalid_flavor):
    with pytest.raises(
        ValueError,
        match=f"^{invalid_flavor} is not a valid RegexFlavor$",
    ):
        RegexFlavor(invalid_flavor)
