from .base import (
    escape,
    make_exp,
    string_as_exp,
    strings_as_exp,
)
from .utils import (
    char_range,
    char_to_cpoint,
    cpoint_to_ord,
    iter_char_range,
    mask_span,
    mask_spans,
    ord_to_cpoint,
    to_nfc,
    to_utf8,
)

__version__ = "0.1.0"

__all__ = [
    "char_range",
    "char_to_cpoint",
    "cpoint_to_ord",
    "escape",
    "iter_char_range",
    "make_exp",
    "mask_span",
    "mask_spans",
    "ord_to_cpoint",
    "string_as_exp",
    "strings_as_exp",
    "to_nfc",
    "to_utf8",
]
