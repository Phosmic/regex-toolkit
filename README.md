# Regex-Toolkit

[Regex-Toolkit](https://github.com/Phosmic/regex-toolkit) Effortlessly craft efficient [RE](https://docs.python.org/3/library/re.html) and [RE2](https://github.com/google/re2) expressions with user-friendly tools.

---

## Requirements:

**Regex-Toolkit** requires Python 3.10 or higher, is platform independent, and has no outside dependencies.

## Issue reporting

If you discover an issue with Regex-Toolkit, please report it at [https://github.com/Phosmic/regex-toolkit/issues](https://github.com/Phosmic/regex-toolkit/issues).

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

---

[Requirements](#requirements)
[Installing](#installing)
[Usage](#usage)
[Library](#library)

## Installing

Most stable version from [**PyPi**](https://pypi.org/project/regex-toolkit/):

[![PyPI](https://img.shields.io/pypi/v/regex-toolkit?style=flat-square)](https://pypi.org/project/regex-toolkit/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/regex-toolkit?style=flat-square)](https://pypi.org/project/regex-toolkit/)
[![PyPI - License](https://img.shields.io/pypi/l/regex-toolkit?style=flat-square)](https://pypi.org/project/regex-toolkit/)

```bash
python3 -m pip install regex-toolkit
```

Development version from [**GitHub**](https://github.com/Phosmic/regex-toolkit):


![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Phosmic/regex-toolkit/ubuntu.yml?style=flat-square)
![Codecov](https://img.shields.io/codecov/c/github/Phosmic/regex-toolkit/master?flag=unittests&style=flat-square&token=XMJZIW8ZL3)
![GitHub](https://img.shields.io/github/license/Phosmic/regex-toolkit?style=flat-square)


```bash
git clone git+https://github.com/Phosmic/regex-toolkit.git
cd regex-toolkit
python3 -m pip install -e .
```

---

## Usage

Import packages:

```python
import re
# and/or
import re2
```

```python
import regex_toolkit
```

---

## Library

<a id="regex_toolkit.base"></a>

# `regex_toolkit.base`

<a id="regex_toolkit.base.iter_sort_by_len"></a>

#### `iter_sort_by_len`

```python
def iter_sort_by_len(texts: Iterable[str],
                     *,
                     reverse: bool = False) -> Iterable[str]
```

Iterate strings sorted by length.

**Arguments**:

- `texts` _Iterable[str]_ - Strings to sort.
- `reverse` _bool, optional_ - Sort in descending order (longest to shortest). Defaults to False.

**Yields**:

- _str_ - Strings sorted by length.

<a id="regex_toolkit.base.sort_by_len"></a>

#### `sort_by_len`

```python
def sort_by_len(texts: Iterable[str],
                *,
                reverse: bool = False) -> tuple[str, ...]
```

Sort strings by length.

**Arguments**:

- `texts` _Iterable[str]_ - Strings to sort.
- `reverse` _bool, optional_ - Sort in descending order (longest to shortest). Defaults to False.

**Returns**:

- _tuple[str]_ - Strings sorted by length.

<a id="regex_toolkit.base.ord_to_codepoint"></a>

#### `ord_to_codepoint`

```python
def ord_to_codepoint(ordinal: int) -> str
```

Character codepoint from character ordinal.

**Arguments**:

- `ordinal` _int_ - Character ordinal.

**Returns**:

- _str_ - Character codepoint.

<a id="regex_toolkit.base.codepoint_to_ord"></a>

#### `codepoint_to_ord`

```python
def codepoint_to_ord(codepoint: str) -> int
```

Character ordinal from character codepoint.

**Arguments**:

- `codepoint` _str_ - Character codepoint.

**Returns**:

- _int_ - Character ordinal.

<a id="regex_toolkit.base.char_to_codepoint"></a>

#### `char_to_codepoint`

```python
def char_to_codepoint(char: str) -> str
```

Character codepoint from character.

**Arguments**:

- `char` _str_ - Character.

**Returns**:

- _str_ - Character codepoint.

<a id="regex_toolkit.base.char_as_exp"></a>

#### `char_as_exp`

```python
def char_as_exp(char: str) -> str
```

Create a RE regex expression that exactly matches a character.

Escape to avoid reserved character classes (i.e. \\s, \\S, \\d, \\D, \\1, etc.).

**Arguments**:

- `char` _str_ - Character to match.

**Returns**:

- _str_ - RE expression that exactly matches the original character.

<a id="regex_toolkit.base.char_as_exp2"></a>

#### `char_as_exp2`

```python
def char_as_exp2(char: str) -> str
```

Create a RE2 regex expression that exactly matches a character.

**Arguments**:

- `char` _str_ - Character to match.

**Returns**:

- _str_ - RE2 expression that exactly matches the original character.

<a id="regex_toolkit.base.string_as_exp"></a>

#### `string_as_exp`

```python
def string_as_exp(text: str) -> str
```

Create a RE regex expression that exactly matches a string.

**Arguments**:

- `text` _str_ - String to match.

**Returns**:

- _str_ - RE expression that exactly matches the original string.

<a id="regex_toolkit.base.string_as_exp2"></a>

#### `string_as_exp2`

```python
def string_as_exp2(text: str) -> str
```

Create a RE2 regex expression that exactly matches a string.

**Arguments**:

- `text` _str_ - String to match.

**Returns**:

- _str_ - RE2 expression that exactly matches the original string.

<a id="regex_toolkit.base.strings_as_exp"></a>

#### `strings_as_exp`

```python
def strings_as_exp(texts: Iterable[str]) -> str
```

Create a RE regex expression that exactly matches any one string.

**Arguments**:

- `texts` _Iterable[str]_ - Strings to match.

**Returns**:

- _str_ - RE expression that exactly matches any one of the original strings.

<a id="regex_toolkit.base.strings_as_exp2"></a>

#### `strings_as_exp2`

```python
def strings_as_exp2(texts: Iterable[str]) -> str
```

Create a RE2 regex expression that exactly matches any one string.

**Arguments**:

- `texts` _Iterable[str]_ - Strings to match.

**Returns**:

- _str_ - RE2 expression that exactly matches any one of the original strings.

<a id="regex_toolkit.base.iter_char_range"></a>

#### `iter_char_range`

```python
def iter_char_range(first_codepoint: int,
                    last_codepoint: int) -> Iterable[str]
```

Iterate all character within a range of codepoints (inclusive).

**Arguments**:

- `first_codepoint` _int_ - Starting (first) codepoint.
- `last_codepoint` _int_ - Ending (last) codepoint.

**Yields**:

- _str_ - Character from within a range of codepoints.

<a id="regex_toolkit.base.char_range"></a>

#### `char_range`

```python
def char_range(first_codepoint: int, last_codepoint: int) -> tuple[str, ...]
```

Tuple of all character within a range of codepoints (inclusive).

**Arguments**:

- `first_codepoint` _int_ - Starting (first) codepoint.
- `last_codepoint` _int_ - Ending (last) codepoint.

**Returns**:

  tuple[str, ...]: Characters within a range of codepoints.

<a id="regex_toolkit.base.mask_span"></a>

#### `mask_span`

```python
def mask_span(text: str,
              span: list[int] | tuple[int, int],
              mask: str | None = None) -> str
```

Slice and mask a string using a single span.

**Arguments**:

- `text` _str_ - String to slice.
- `span` _list[int] | tuple[int, int]_ - Domain of index positions (start, end) to mask.
- `mask` _str, optional_ - Mask to insert after slicing. Defaults to None.

**Returns**:

- _str_ - String with span replaced with the mask text.

<a id="regex_toolkit.base.mask_spans"></a>

#### `mask_spans`

```python
def mask_spans(text: str,
               spans: Iterable[list[int] | tuple[int, int]],
               masks: Iterable[str] | None = None) -> str
```

Slice and mask a string using multiple spans.

**Arguments**:

- `text` _str_ - String to slice.
- `spans` _Iterable[list[int] | tuple[int, int]]_ - Domains of index positions (x1, x2) to mask from the text.
- `masks` _Iterable[str], optional_ - Masks to insert when slicing. Defaults to None.

**Returns**:

- _str_ - String with all spans replaced with the mask text.

<a id="regex_toolkit.base.to_nfc"></a>

#### `to_nfc`

```python
def to_nfc(text: str) -> str
```

Normalize a Unicode string to NFC form C.

Form C favors the use of a fully combined character.

**Arguments**:

- `text` _str_ - String to normalize.

**Returns**:

- _str_ - Normalized string.

<a id="regex_toolkit.base_BAK_2022-11-18"></a>

# `regex_toolkit.base_BAK_2022-11-18`

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit"></a>

## `RegexToolkit` Objects

```python
class RegexToolkit()
```

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.char_as_exp"></a>

#### `RegexToolkit.char_as_exp`

```python
@staticmethod
def char_as_exp(char: str) -> str
```

Create a re Regex Expression that Exactly Matches a Character

Expressions like \s, \S, \d, \D, \1, etc. are reserved.

**Arguments**:

- `char` _str_ - Character to match.

**Returns**:

- _str_ - re expression that exactly matches the original character.

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.char_as_exp2"></a>

#### `RegexToolkit.char_as_exp2`

```python
@staticmethod
def char_as_exp2(char: str) -> str
```

Create a re2 Regex Expression that Exactly Matches a Character

**Arguments**:

- `char` _str_ - Character to match.

**Returns**:

- _str_ - re2 expression that exactly matches the original character.

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.string_as_exp"></a>

#### `RegexToolkit.string_as_exp`

```python
@staticmethod
def string_as_exp(text: str) -> str
```

Create a re Regex Expression that Exactly Matches a String

**Arguments**:

- `text` _str_ - String to match.

**Returns**:

- _str_ - re expression that exactly matches the original string.

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.string_as_exp2"></a>

#### `RegexToolkit.string_as_exp2`

```python
@staticmethod
def string_as_exp2(text: str) -> str
```

Create a re2 Regex Expression that Exactly Matches a String

**Arguments**:

- `text` _str_ - String to match.

**Returns**:

- _str_ - re2 expression that exactly matches the original string.

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.strings_as_exp"></a>

#### `RegexToolkit.strings_as_exp`

```python
@staticmethod
def strings_as_exp(texts: Iterable[str]) -> str
```

re

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.strings_as_exp2"></a>

#### `RegexToolkit.strings_as_exp2`

```python
@staticmethod
def strings_as_exp2(texts: Iterable[str]) -> str
```

re2

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.iter_char_range"></a>

#### `RegexToolkit.iter_char_range`

```python
@staticmethod
def iter_char_range(first_codepoint: int,
                    last_codepoint: int) -> Iterable[str]
```

Iterate All Characters within a Range of Codepoints (Inclusive)

**Arguments**:

- `first_codepoint` _int_ - Starting codepoint.
- `last_codepoint` _int_ - Final codepoint.

**Yields**:

- _str_ - Character from within a range of codepoints.

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.char_range"></a>

#### `RegexToolkit.char_range`

```python
@staticmethod
def char_range(first_codepoint: int, last_codepoint: int) -> tuple[str, ...]
```

Tuple of All Characters within a Range of Codepoints (Inclusive)

**Arguments**:

- `first_codepoint` _int_ - Starting codepoint.
- `last_codepoint` _int_ - Final codepoint.

**Returns**:

  tuple[str, ...]: Characters within a range of codepoints.

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.is_digit"></a>

#### `RegexToolkit.is_digit`

```python
@staticmethod
def is_digit(char: str) -> bool
```

Check if a Character is a Digit [0-9]

**Arguments**:

- `char` _str_ - Character to check.

**Returns**:

- _bool_ - True if the character is a digit.

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.mask_span"></a>

#### `RegexToolkit.mask_span`

```python
@staticmethod
def mask_span(text: str, span, mask: str | None = None) -> str
```

Slice and Mask Text using a Span

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.mask_spans"></a>

#### `RegexToolkit.mask_spans`

```python
@staticmethod
def mask_spans(text: str, spans: Iterable[Sequence[int]],
               masks: Iterable[str]) -> str
```

Slice and Mask a String using Multiple Spans

NOTE: Original values for spans and masks parameters will be modified!

**Arguments**:

- `text` _str_ - Text to slice.
- `spans` _Spans_ - Domains of index positions to mask from the text.
- `masks` _Masks, optional_ - Masks to insert when slicing. Defaults to None.

**Returns**:

- _str_ - Text with all spans replaced with the mask text.

<a id="regex_toolkit.base_BAK_2022-11-18.RegexToolkit.to_utf8"></a>

#### `RegexToolkit.to_utf8`

```python
@staticmethod
def to_utf8(text: str) -> str
```

Force UTF-8 Text Encoding

**Arguments**:

- `text` _str_ - Text to encode.

**Returns**:

- _str_ - Encoded text.


---

