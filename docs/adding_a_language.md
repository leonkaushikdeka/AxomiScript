# Adding a New Language to AxomiScript

This guide walks you through adding a new natural-language frontend (e.g., Hindi, Bengali, Bodo) to the AxomiScript language registry. Each frontend is an independent Python package under `axomiscript/languages/`.

---

## Overview

AxomiScript uses a plugin architecture: every language frontend parses its own source syntax and produces the same shared AST nodes defined in `axomiscript/core/ast_nodes.py`. The code generators (Python 3, C++17) work entirely against those shared nodes, so a new language gets both targets for free.

---

## Step 1 — Create the package directory

```
axomiscript/languages/<name>/
    __init__.py
    keywords.py
    preprocessor.py
    grammar.py
    transformer.py
    parser.py
```

Replace `<name>` with a lowercase identifier for your language (e.g., `hindi`, `bengali`, `bodo`).

---

## Step 2 — Define `keywords.py`

`keywords.py` maps the six semantic roles to words in the target language.
It also provides a digit-translation table if the language uses a non-ASCII numeral system.

**Required keys** (exact spelling matters — the grammar uses them by name):

| Key     | Semantic role              |
|---------|----------------------------|
| `VAR`   | Variable declaration       |
| `IF`    | Conditional (if)           |
| `ELSE`  | Conditional (else)         |
| `LOOP`  | Counted loop               |
| `PRINT` | Print / output             |
| `TO`    | Range end (e.g., 1 to 5)  |

### Hindi example

```python
# axomiscript/languages/hindi/keywords.py
# -*- coding: utf-8 -*-

KEYWORDS = {
    "VAR":   "चर",         # variable
    "IF":    "अगर",        # if
    "ELSE":  "नहीं_तो",    # else
    "LOOP":  "चक्र",       # loop
    "PRINT": "प्रिंट",     # print
    "TO":    "तक",         # to / up-to
}

# Devanagari → ASCII digit mapping
DEVANAGARI_TO_ASCII = str.maketrans("०१२३४५६७८९", "0123456789")
```

### Bodo example

```python
# axomiscript/languages/bodo/keywords.py
# -*- coding: utf-8 -*-

KEYWORDS = {
    "VAR":   "मोजाब",   # variable
    "IF":    "यदि",      # if
    "ELSE":  "नैसे",     # else
    "LOOP":  "चक्र",     # loop
    "PRINT": "दिखाउ",   # print
    "TO":    "लानाय",   # to / up-to
}

# Bodo is written in Devanagari; reuse the same digit table
DEVANAGARI_TO_ASCII = str.maketrans("०१२३४५६७८९", "0123456789")
```

> **Tip:** If your language uses ASCII digits already, set the translation table to `str.maketrans("", "")` (an identity mapping) or simply skip `preprocess()`.

---

## Step 3 — Create `preprocessor.py`

The preprocessor converts non-ASCII digits to ASCII before the grammar runs its `NUMBER` terminal.

```python
# axomiscript/languages/hindi/preprocessor.py
# -*- coding: utf-8 -*-
from .keywords import DEVANAGARI_TO_ASCII

def preprocess(source: str) -> str:
    """Replace Devanagari numerals with ASCII equivalents."""
    return source.translate(DEVANAGARI_TO_ASCII)
```

If your language uses purely ASCII digits, this can be a no-op:

```python
def preprocess(source: str) -> str:
    return source
```

---

## Step 4 — Create `grammar.py`

Copy the grammar pattern from the Assamese reference implementation. The only thing you change is which `keywords` module you import. The `_GRAMMAR_BASE` string is **identical** for every language.

```python
# axomiscript/languages/hindi/grammar.py
# -*- coding: utf-8 -*-
from lark import Lark
from .keywords import KEYWORDS

_GRAMMAR_BASE = (
    "start        : statement+\n"
    "statement    : var_decl | print_stmt | if_stmt | loop_stmt\n"
    'var_decl     : KW_VAR IDENT "=" expr NEWLINE\n'
    "print_stmt   : KW_PRINT expr NEWLINE\n"
    'if_stmt      : KW_IF expr "{" NEWLINE statement+ "}" NEWLINE? else_clause?\n'
    'else_clause  : KW_ELSE "{" NEWLINE statement+ "}" NEWLINE?\n'
    'loop_stmt    : KW_LOOP IDENT "=" expr KW_TO expr "{" NEWLINE statement+ "}" NEWLINE?\n'
    "expr         : comparison\n"
    "comparison   : arith (CMP_OP arith)*\n"
    "arith        : term  (ADD_OP  term )*\n"
    "term         : factor (MUL_OP factor)*\n"
    "factor       : NUMBER | STRING | IDENT\n"
    'CMP_OP       : "==" | "!=" | ">=" | "<=" | ">" | "<"\n'
    'ADD_OP       : "+" | "-"\n'
    'MUL_OP       : "*" | "/"\n'
    "NUMBER       : /[0-9]+(\\.[0-9]+)?/\n"
    'STRING       : /\"[^\"]*\"/\n'
    "IDENT        : /[\u0900-\u097Fa-zA-Z_][\u0900-\u097Fa-zA-Z0-9_]*/\n"
    "NEWLINE      : /\\r?\\n/\n"
    "%ignore /[^\\S\\r\\n]+/\n"
)

_GRAMMAR = _GRAMMAR_BASE + "".join(
    f"KW_{name}.10 : /{word}/\n"
    for name, word in KEYWORDS.items()
)

PARSER = Lark(_GRAMMAR, parser="earley", ambiguity="resolve")
```

**IDENT Unicode range notes:**

| Script      | Unicode block  | Range           |
|-------------|----------------|-----------------|
| Assamese / Bengali | Bengali | `\u0980-\u09FF` |
| Devanagari (Hindi, Bodo, Maithili) | Devanagari | `\u0900-\u097F` |
| Odia        | Oriya          | `\u0B00-\u0B7F` |
| Tamil       | Tamil          | `\u0B80-\u0BFF` |

Update the IDENT regex to cover whichever Unicode block your language uses.

---

## Step 5 — Create `transformer.py`

Subclass `AssameseTransformer`. You only need to override or add `KW_*` terminal handlers if you have extra/different keywords. All statement and expression rules are inherited.

```python
# axomiscript/languages/hindi/transformer.py
# -*- coding: utf-8 -*-
from ...languages.assamese.transformer import AssameseTransformer

class HindiTransformer(AssameseTransformer):
    """
    Inherits all transformation logic from AssameseTransformer.
    KW_* methods discard their tokens and are already defined in the parent.
    No overrides needed unless you add language-specific syntax.
    """
    pass
```

If your language introduces additional keywords (e.g., a `FUNCTION` keyword), add the corresponding `KW_FUNCTION` method that returns `None` (to discard the token) and extend the transformer logic as needed.

---

## Step 6 — Create `parser.py`

```python
# axomiscript/languages/hindi/parser.py
# -*- coding: utf-8 -*-
from __future__ import annotations
from ...core.ast_nodes import Program
from .preprocessor import preprocess
from .grammar import PARSER
from .transformer import HindiTransformer

_TRANSFORMER = HindiTransformer()

def parse(source: str) -> Program:
    """
    Parse AxomiScript (Hindi) source code into a typed AST.

    Parameters
    ----------
    source : str
        UTF-8 source code using Hindi keywords and optional Devanagari numerals.

    Returns
    -------
    Program
        Root AST node.
    """
    normalised = preprocess(source)
    if not normalised.endswith("\n"):
        normalised += "\n"
    cst = PARSER.parse(normalised)
    return _TRANSFORMER.transform(cst)
```

---

## Step 7 — Create `__init__.py`

```python
# axomiscript/languages/hindi/__init__.py
# -*- coding: utf-8 -*-
"""Hindi (हिन्दी) language frontend for AxomiScript."""
from .parser import parse

__all__ = ["parse"]
```

---

## Step 8 — Register in the language registry

Open `axomiscript/languages/__init__.py` and add two lines at the bottom of the "Auto-register bundled languages" section:

```python
# ── Auto-register bundled languages ─────────────────────────────────────
from .assamese import parse as _assamese_parse  # noqa: E402
register("assamese", _assamese_parse)

from .hindi import parse as _hindi_parse        # noqa: E402  ← ADD THIS
register("hindi", _hindi_parse)                 #             ← AND THIS
```

After this, `axomiscript.available()` will return `['assamese', 'hindi']` and the CLI flag `--lang hindi` will work automatically.

---

## Complete Hindi example

Once all files are in place, a Hindi AxomiScript program would look like:

```
चर क = १०
अगर क > ५ {
    प्रिंट "बड़ा"
}
नहीं_तो {
    प्रिंट "छोटा"
}
चक्र ई = १ तक ३ {
    प्रिंट ई
}
```

Compile it with:

```bash
python -m axomiscript --lang hindi --file program_hi.as
```

---

## Testing your new language

Add a `tests/test_hindi.py` file that mirrors `tests/test_assamese.py`, replacing all Assamese source strings with valid Hindi source strings. Run:

```bash
pytest tests/test_hindi.py -v
```

At minimum, cover:
- Variable declaration
- Print statement
- If / else
- Loop
- Pipeline round-trip (`run(src, language="hindi", verbose=False)`)

---

## Checklist

- [ ] `keywords.py` — all six keys defined, digit map present if needed
- [ ] `preprocessor.py` — converts script-specific digits to ASCII
- [ ] `grammar.py` — correct Unicode range in `IDENT` terminal
- [ ] `transformer.py` — subclasses `AssameseTransformer` (or defines its own)
- [ ] `parser.py` — `parse(source) -> Program` is the public API
- [ ] `__init__.py` — exposes `parse`
- [ ] Registered in `axomiscript/languages/__init__.py`
- [ ] At least one test file under `tests/`
- [ ] All `.py` files have `# -*- coding: utf-8 -*-` header
