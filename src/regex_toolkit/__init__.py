from .base import (
    escape,
    make_exp,
    string_as_exp,
    strings_as_exp,
)
from .enums import RegexFlavor
from .utils import (
    char_range,
    char_to_cpoint,
    cpoint_to_ord,
    iter_char_range,
    iter_sort_by_len,
    mask_span,
    mask_spans,
    ord_to_cpoint,
    sort_by_len,
    to_nfc,
    to_utf8,
)

__version__ = "0.0.5"

__all__ = [
    "char_range",
    "char_to_cpoint",
    "cpoint_to_ord",
    "escape",
    "iter_char_range",
    "iter_sort_by_len",
    "make_exp",
    "mask_span",
    "mask_spans",
    "ord_to_cpoint",
    "RegexFlavor",
    "sort_by_len",
    "string_as_exp",
    "strings_as_exp",
    "to_nfc",
    "to_utf8",
]
