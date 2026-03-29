# -*- coding: utf-8 -*-
"""Public parse() function for Assamese source code."""
from __future__ import annotations
from ...core.ast_nodes import Program
from .preprocessor import preprocess
from .grammar import PARSER
from .transformer import AssameseTransformer

_TRANSFORMER = AssameseTransformer()


def parse(source: str) -> Program:
    """
    Parse AxomiScript (Assamese) source code into a typed AST.

    Steps
    -----
    1. preprocess()        — Nagari digits → ASCII
    2. PARSER.parse()      — Earley parser → CST
    3. _TRANSFORMER.transform() — CST → AST

    Parameters
    ----------
    source : str
        UTF-8 AxomiScript source. May contain Eastern Nagari numerals.

    Returns
    -------
    Program
        Root AST node.

    Raises
    ------
    lark.exceptions.UnexpectedInput
        On syntax errors, with line/column information.
    """
    normalised = preprocess(source)
    if not normalised.endswith("\n"):
        normalised += "\n"
    cst = PARSER.parse(normalised)
    return _TRANSFORMER.transform(cst)
