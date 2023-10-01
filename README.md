# Regex-Toolkit

[Regex-Toolkit](https://github.com/Phosmic/regex-toolkit) provides tools for creating [RE](https://docs.python.org/3/library/re.html) and [RE2](https://github.com/google/re2) expressions.

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
![Codecov](https://img.shields.io/codecov/c/github/Phosmic/regex-toolkit/main?flag=unittests&style=flat-square&token=NOT_YET_CONFIGURED)
![GitHub](https://img.shields.io/github/license/Phosmic/regex-toolkit?style=flat-square)


```bash
git clone git+https://github.com/Phosmic/regex-toolkit.git
cd regex-toolkit
python3 -m pip install -e .
```

---

## Usage

To harness the toolkit's capabilities, you should import the necessary packages:

```python
import re
# and/or
import re2
import regex_toolkit as rtk
```

### Why Use `regex_toolkit`?

Regex definitions vary across languages and versions.
By using the toolkit, you can achieve a more consistent and comprehensive representation of unicode support.
It is especially useful to supplement base unicode sets with the latest definitions from other languages and standards.

### RE2 Overview

RE2 focuses on safely processing regular expressions, particularly from untrusted inputs.
It ensures both linear match time and efficient memory usage.
Although it might not always surpass other engines in speed, it intentionally omits features that depend solely on backtracking, like backreferences and look-around assertions.

A brief rundown of RE2 terminology:

- **BitState**: An execution engine that uses backtracking search.
- **bytecode**: The set of instructions that form an automaton.
- **DFA**: The engine for Deterministic Finite Automaton searches.
- **NFA**: Implements the Nondeterministic Finite Automaton search method.
- **OnePass**: A one-pass search execution engine.
- **pattern**: The textual form of a regex.
- **Prog**: The compiled version of a regex.
- **Regexp**: The parsed version of a regex.
- **Rune**: A character in terms of encoding, essentially a code point.

For an in-depth exploration, please refer to the [RE2 documentation](https://github.com/google/re2/wiki/Glossary).

---

## Library

<a id="regex_toolkit.utils"></a>

# `regex_toolkit.utils`

<a id="regex_toolkit.utils.resolve_flavor"></a>

#### `resolve_flavor`

```python
def resolve_flavor(potential_flavor: int | RegexFlavor | None) -> RegexFlavor
```

Resolve a regex flavor.

If the flavor is an integer, it is validated and returned.
If the flavor is a RegexFlavor, it is returned.
If the flavor is None, the default flavor is returned. To change the default flavor, set `default_flavor`.

```python
import regex_toolkit as rtk

rtk.base.default_flavor = 2
assert rtk.utils.resolve_flavor(None) == rtk.enums.RegexFlavor.RE2
```

**Arguments**:

- `potential_flavor` _int | RegexFlavor | None_ - Potential regex flavor.

**Returns**:

- _RegexFlavor_ - Resolved regex flavor.

**Raises**:

- `ValueError` - Invalid regex flavor.

<a id="regex_toolkit.utils.iter_sort_by_len"></a>

#### `iter_sort_by_len`

```python
def iter_sort_by_len(texts: Iterable[str],
                     *,
                     reverse: bool = False) -> Generator[str, None, None]
```

Iterate strings sorted by length.

**Arguments**:

- `texts` _Iterable[str]_ - Strings to sort.
- `reverse` _bool, optional_ - Sort in descending order (longest to shortest). Defaults to False.

**Yields**:

- _str_ - Strings sorted by length.

<a id="regex_toolkit.utils.sort_by_len"></a>

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

- _tuple[str, ...]_ - Strings sorted by length.

<a id="regex_toolkit.utils.ord_to_cpoint"></a>

#### `ord_to_cpoint`

```python
def ord_to_cpoint(ordinal: int) -> str
```

Character ordinal to character codepoint.

The codepoint is always 8 characters long (zero-padded).

**Example**:

```python
ord_to_cpoint(97)
# Output: '00000061'
```

**Arguments**:

- `ordinal` _int_ - Character ordinal.

**Returns**:

- _str_ - Character codepoint.

<a id="regex_toolkit.utils.cpoint_to_ord"></a>

#### `cpoint_to_ord`

```python
def cpoint_to_ord(cpoint: str) -> int
```

Character codepoint to character ordinal.

**Arguments**:

- `cpoint` _str_ - Character codepoint.

**Returns**:

- _int_ - Character ordinal.

<a id="regex_toolkit.utils.char_to_cpoint"></a>

#### `char_to_cpoint`

```python
def char_to_cpoint(char: str) -> str
```

Character to character codepoint.

**Example**:

```python
char_to_cpoint("a")
# Output: '00000061'
```

**Arguments**:

- `char` _str_ - Character.

**Returns**:

- _str_ - Character codepoint.

<a id="regex_toolkit.utils.to_nfc"></a>

#### `to_nfc`

```python
def to_nfc(text: str) -> str
```

Normalize a Unicode string to NFC form C.

Form C favors the use of a fully combined character.

**Example**:

```python
to_nfc("e\\u0301") == "é"
# Output: True
```

**Arguments**:

- `text` _str_ - String to normalize.

**Returns**:

- _str_ - Normalized string.

<a id="regex_toolkit.utils.iter_char_range"></a>

#### `iter_char_range`

```python
def iter_char_range(first_char: str,
                    last_char: str) -> Generator[str, None, None]
```

Iterate all characters within a range of characters (inclusive).

**Example**:

```python
char_range("a", "c")
# Output: ('a', 'b', 'c')

char_range("c", "a")
# Output: ('c', 'b', 'a')
```

**Arguments**:

- `first_char` _str_ - Starting (first) character.
- `last_char` _str_ - Ending (last) character.

**Yields**:

- _str_ - Characters within a range of characters.

<a id="regex_toolkit.utils.char_range"></a>

#### `char_range`

```python
def char_range(first_char: str, last_char: str) -> tuple[str, ...]
```

Tuple of all characters within a range of characters (inclusive).

**Example**:

```python
char_range("a", "d")
# Output: ('a', 'b', 'c', 'd')

char_range("d", "a")
# Output: ('d', 'c', 'b', 'a')
```

**Arguments**:

- `first_char` _str_ - Starting (first) character.
- `last_char` _str_ - Ending (last) character.

**Returns**:

- _tuple[str, ...]_ - Characters within a range of characters.

<a id="regex_toolkit.utils.mask_span"></a>

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

<a id="regex_toolkit.utils.mask_spans"></a>

#### `mask_spans`

```python
def mask_spans(text: str,
               spans: Iterable[list[int] | tuple[int, int]],
               masks: Iterable[str] | None = None) -> str
```

Slice and mask a string using multiple spans.

Todo: Add support for overlapping (and unordered?) spans.

**Arguments**:

- `text` _str_ - String to slice.
- `spans` _Iterable[list[int] | tuple[int, int]]_ - Domains of index positions (x1, x2) to mask within the text.
- `masks` _Iterable[str], optional_ - Masks to insert when slicing. Defaults to None.

**Returns**:

- _str_ - String with all spans replaced with the mask text.

<a id="regex_toolkit.base"></a>

# `regex_toolkit.base`

<a id="regex_toolkit.base.escape"></a>

#### `escape`

```python
def escape(char: str, flavor: int | None = None) -> str
```

Create a regex expression that exactly matches a character.

**Arguments**:

- `char` _str_ - Character to match.
- `flavor` _int | None, optional_ - Regex flavor (1 for RE, 2 for RE2). Defaults to None.

**Returns**:

- _str_ - Expression that exactly matches the original character.

**Raises**:

- `ValueError` - Invalid regex flavor.

<a id="regex_toolkit.base.string_as_exp"></a>

#### `string_as_exp`

```python
def string_as_exp(text: str, flavor: int | None = None) -> str
```

Create a regex expression that exactly matches a string.

**Arguments**:

- `text` _str_ - String to match.
- `flavor` _int | None, optional_ - Regex flavor (1 for RE, 2 for RE2). Defaults to None.

**Returns**:

- _str_ - Expression that exactly matches the original string.

**Raises**:

- `ValueError` - Invalid regex flavor.

<a id="regex_toolkit.base.strings_as_exp"></a>

#### `strings_as_exp`

```python
def strings_as_exp(texts: Iterable[str], flavor: int | None = None) -> str
```

Create a regex expression that exactly matches any one string.

**Arguments**:

- `texts` _Iterable[str]_ - Strings to match.
- `flavor` _int | None, optional_ - Regex flavor (1 for RE, 2 for RE2). Defaults to None.

**Returns**:

- _str_ - Expression that exactly matches any one of the original strings.

**Raises**:

- `ValueError` - Invalid regex flavor.

<a id="regex_toolkit.base.make_exp"></a>

#### `make_exp`

```python
def make_exp(chars: Iterable[str], flavor: int | None = None) -> str
```

Create a regex expression that exactly matches a list of characters.

The characters are sorted and grouped into ranges where possible.
The expression is not anchored, so it can be used as part of a larger expression.

**Example**:

```python
exp = "[" + make_exp(["a", "b", "c", "z", "y", "x"]) + "]"
# Output: '[a-cx-z]'
```

**Arguments**:

- `chars` _Iterable[str]_ - Characters to match.
- `flavor` _int | None, optional_ - Regex flavor (1 for RE, 2 for RE2). Defaults to None.

**Returns**:

- _str_ - Expression that exactly matches the original characters.

**Raises**:

- `ValueError` - Invalid regex flavor.

<a id="regex_toolkit.enums"></a>

# `regex_toolkit.enums`

Enums.

<a id="regex_toolkit.enums.RegexFlavor"></a>

## `RegexFlavor` Objects

```python
class RegexFlavor(int, Enum)
```

Regex flavors.

**Attributes**:

- `RE` _int_ - Standard Python regex flavor.
- `RE2` _int_ - Google RE2 regex flavor.


---

