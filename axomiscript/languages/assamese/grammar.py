# -*- coding: utf-8 -*-
r"""
Lark grammar for Assamese (AxomiScript).

KEY DESIGN: Keyword terminals are injected at runtime using an f-string so
the actual Unicode characters are embedded directly inside the /regex/
terminal patterns.  Writing them as r-string escape sequences (\u09xx)
inside a raw triple-quoted block would cause Lark to treat them as literal
backslash-u sequences and fail to match Assamese text.
"""
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
    "IDENT        : /[\u0980-\u09FFa-zA-Z_][\u0980-\u09FFa-zA-Z0-9_]*/\n"
    "NEWLINE      : /\\r?\\n/\n"
    "%ignore /[^\\S\\r\\n]+/\n"
)

# Append one terminal per keyword, embedding the real Unicode character
_GRAMMAR = _GRAMMAR_BASE + "".join(
    f"KW_{name}.10 : /{word}/\n"
    for name, word in KEYWORDS.items()
)

PARSER = Lark(_GRAMMAR, parser="earley", ambiguity="resolve")
