# Regex-Toolkit

[Regex-Toolkit](https://github.com/Phosmic/regex-toolkit): Effortlessly craft efficient [RE](https://docs.python.org/3/library/re.html) and [RE2](https://github.com/google/re2) expressions with user-friendly tools.

## Requirements:

**Regex-Toolkit** requires Python 3.9 or higher, is platform independent, and has no outside dependencies.

## Issue reporting

If you discover an issue with Regex-Toolkit, please report it at [https://github.com/Phosmic/regex-toolkit/issues](https://github.com/Phosmic/regex-toolkit/issues).

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

---

## Installing

Most stable version from [**PyPi**](https://pypi.org/project/regex-toolkit/):

```bash
pip install regex-toolkit
```

Development version from [**GitHub**](https://github.com/Phosmic/regex-toolkit):

```bash
git clone git+https://github.com/Phosmic/regex-toolkit.git
cd regex-toolkit
pip install .
```

## Usage

Import packages:

```python
import re
# and/or
import re2
```

```python
# Can import directly if desired
import regex_toolkit as rtk
```

---

## Library

### iter_sort_by_len

Function to iterate strings sorted by length.

| Function Signature                                |
| :------------------------------------------------ |
| iter_sort_by_len(package_name, \*, reverse=False) |

| Parameters                 |                                                 |
| :------------------------- | :---------------------------------------------- |
| **texts**_(Iterable[str])_ | Strings to sort.                                |
| **reverse**_(int)_         | Sort in descending order (longest to shortest). |

Example (ascending shortest to longest):

```python
words = ["longest", "short", "longer"]
for word in rtk.iter_sort_by_len(words):
    print(word)
```

Output:

```text
short
longer
longest
```

Example reversed (descending longest to shortest):

```python
words = ["longest", "short", "longer"]
for word in rtk.iter_sort_by_len(words, reverse=True):
    print(word)
```

Output:

```text
longest
longer
short
```

### sort_by_len

Function to get a tuple of strings sorted by length.

| Function Signature                           |
| :------------------------------------------- |
| sort_by_len(package_name, \*, reverse=False) |

| Parameters                 |                                                 |
| :------------------------- | :---------------------------------------------- |
| **texts**_(Iterable[str])_ | Strings to sort.                                |
| **reverse**_(int)_         | Sort in descending order (longest to shortest). |

Example (ascending shortest to longest):

```python
rtk.sort_by_len(["longest", "short", "longer"])
```

Result:

```python
('short', 'longer', 'longest')
```

Example reversed (descending longest to shortest):

```python
rtk.sort_by_len(["longest", "short", "longer"], reverse=True)
```

Result:

```python
('longest', 'longer', 'short')
```

### ord_to_codepoint

Function to get a character codepoint from a character ordinal.

| Function Signature        |
| :------------------------ |
| ord_to_codepoint(ordinal) |

| Parameters         |                    |
| :----------------- | :----------------- |
| **ordinal**_(int)_ | Character ordinal. |

Example:

```python
# ordinal: 127344
ordinal = ord("🅰")
rtk.ord_to_codepoint(ordinal)
```

Result:

```python
'0001f170'
```

### codepoint_to_ord

Function to get a character ordinal from a character codepoint.

| Function Signature          |
| :-------------------------- |
| codepoint_to_ord(codepoint) |

| Parameters           |                      |
| :------------------- | :------------------- |
| **codepoint**_(str)_ | Character codepoint. |

Example:

```python
# char: "🅰"
codepoint = "0001f170"
rtk.codepoint_to_ord(codepoint)
```

Result:

```python
127344
```

### char_to_codepoint

Function to get a character codepoint from a character.

| Function Signature      |
| :---------------------- |
| char_to_codepoint(char) |

| Parameters      |            |
| :-------------- | :--------- |
| **char**_(str)_ | Character. |

Example:

```python
rtk.char_to_codepoint("🅰")
```

Result:

```python
'0001f170'
```

### char_as_exp

Function to create a **RE** expression that exactly matches a character.

| Function Signature |
| :----------------- |
| char_as_exp(char)  |

| Parameters      |                     |
| :-------------- | :------------------ |
| **char**_(str)_ | Character to match. |

Example:

```python
rtk.char_as_exp("🅰")
```

Result:

```python
r'\🅰'
```

### char_as_exp2

Function to create a **RE** expression that exactly matches a character.

| Function Signature |
| :----------------- |
| char_as_exp2(char) |

| Parameters      |                     |
| :-------------- | :------------------ |
| **char**_(str)_ | Character to match. |

Example:

```python
rtk.char_as_exp2("🅰")
```

Result:

```python
r'\x{0001f170}'
```

### string_as_exp

Function to create a **RE** expression that exactly matches a string.

| Function Signature  |
| :------------------ |
| string_as_exp(text) |

| Parameters      |                  |
| :-------------- | :--------------- |
| **text**_(str)_ | String to match. |

Example:

```python
rtk.string_as_exp("🅰🅱🅲")
```

Result:

```python
r'\🅰\🅱\🅲'
```

### string_as_exp2

Function to create a **RE** expression that exactly matches a string.

| Function Signature   |
| :------------------- |
| string_as_exp2(text) |

| Parameters      |                  |
| :-------------- | :--------------- |
| **text**_(str)_ | String to match. |

Example:

```python
rtk.string_as_exp2("🅰🅱🅲")
```

Result:

```python
r'\x{0001f170}\x{0001f171}\x{0001f172}'
```

### strings_as_exp

Function to create a **RE** expression that exactly matches any one string.

| Function Signature    |
| :-------------------- |
| strings_as_exp(texts) |

| Parameters                 |                   |
| :------------------------- | :---------------- |
| **texts**_(Iterable[str])_ | Strings to match. |

Example:

```python
rtk.strings_as_exp([
    "bad.word",
    "another-bad-word",
])
```

Result:

```python
r'another\-bad\-word|bad\.word'
```

### strings_as_exp2

Function to create a **RE** expression that exactly matches any one string.

| Function Signature     |
| :--------------------- |
| strings_as_exp2(texts) |

| Parameters                 |                   |
| :------------------------- | :---------------- |
| **texts**_(Iterable[str])_ | Strings to match. |

Example:

```python
rtk.strings_as_exp2([
    "bad.word",
    "another-bad-word",
])
```

Result:

```python
r'another\-bad\-word|bad\.word'
```

### iter_char_range

Function to iterate all characters within a range of codepoints (inclusive).

| Function                                           |
| :------------------------------------------------- |
| iter_char_range(first_codepoint, second_codepoint) |

| Parameters                 |                             |
| :------------------------- | :-------------------------- |
| **first_codepoint**_(int)_ | Starting (first) codepoint. |
| **last_codepoint**_(int)_  | Ending (last) codepoint.    |

Example:

```python
for char in rtk.iter_char_range("a", "c"):
    print(char)
```

Output:

```text
a
b
c
```

### char_range

Function to get a tuple of all characters within a range of codepoints (inclusive).

| Function                                      |
| :-------------------------------------------- |
| char_range(first_codepoint, second_codepoint) |

| Parameters                 |                             |
| :------------------------- | :-------------------------- |
| **first_codepoint**_(int)_ | Starting (first) codepoint. |
| **last_codepoint**_(int)_  | Ending (last) codepoint.    |

Example:

```python
rtk.char_range("a", "c")
```

Result:

```python
('a', 'b', 'c')
```

### mask_span

Slice and mask a string using a span.

| Function Signature               |
| :------------------------------- |
| mask_span(text, span, mask=None) |

| Parameters                               |                                                 |
| :--------------------------------------- | :---------------------------------------------- |
| **text**_(str)_                          | Text to slice.                                  |
| **span**_(list[int] \| tuple[int, int])_ | Domain of index positions (start, end) to mask. |
| **mask**_(str \| None)_                  | Mask to insert after slicing.                   |

Example:

```python
rtk.mask_span(
    "This is an example",
    (8, 8),
    mask="not ",
)
```

Result:

```python
'This is not an example'
```

### mask_spans

Slice and mask a string using multiple spans.

| Function Signature                  |
| :---------------------------------- |
| mask_spans(text, spans, masks=None) |

| Parameters                                          |                                                            |
| :-------------------------------------------------- | :--------------------------------------------------------- |
| **text**_(str)_                                     | Text to slice.                                             |
| **spans**_(Iterable[list[int] \| tuple[int, int]])_ | Domains of index positions (x1, x2) to mask from the text. |
| **masks**_(Iterable[str] \| None)_                  | Masks to insert when slicing.                              |

Example:

```python
rtk.mask_spans(
    "This is an example",
    spans=[
        (9, 10),
        (11, 18),
    ],
    masks=[
        " good",
        "sample",
    ],
)
```

### to_utf8

Encode a unicode string to UTF-8 form.

| Function Signature |
| :----------------- |
| to_utf8(text)      |

| Parameters      |                 |
| :-------------- | :-------------- |
| **text**_(str)_ | Text to encode. |

### to_nfc

[Normalize](https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize) a Unicode string to NFC form C.

| Function Signature |
| :----------------- |
| to_utf8(text)      |

| Parameters      |                    |
| :-------------- | :----------------- |
| **text**_(str)_ | Text to normalize. |
