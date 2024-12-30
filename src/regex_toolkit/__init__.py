from .base import (
    escape,
    make_expr,
    string_as_expr,
    strings_as_expr,
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

__version__ = "0.1.1"

__all__ = [
    "char_range",
    "char_to_cpoint",
    "cpoint_to_ord",
    "escape",
    "iter_char_range",
    "make_expr",
    "mask_span",
    "mask_spans",
    "ord_to_cpoint",
    "string_as_expr",
    "strings_as_expr",
    "to_nfc",
    "to_utf8",
]
