# -*- coding: utf-8 -*-
"""
High-level compiler API: parse → generate → (optionally) execute.

This is the main programmatic API for tools and scripts.
The old pipeline.py is kept for compatibility but compiler.py
is the preferred entry point.
"""
from __future__ import annotations
from .languages import get_parser
from .generators import python_gen, cpp_gen
from .core.utils import pretty_ast


def compile_source(
    source: str,
    language: str = "assamese",
    target: str = "python",
) -> str:
    """
    Compile *source* to the requested *target* language.

    Parameters
    ----------
    source   : str — source code.
    language : str — source language name (default: 'assamese').
    target   : str — 'python' or 'cpp' (default: 'python').

    Returns
    -------
    str — generated source code in the target language.

    Raises
    ------
    ValueError  — if *target* is not recognised.
    lark.exceptions.UnexpectedInput — on syntax errors.
    """
    parse = get_parser(language)
    program = parse(source)

    if target == "python":
        return python_gen.generate(program)
    if target in ("cpp", "c++", "c++17"):
        return cpp_gen.generate(program)
    if target == "ast":
        return pretty_ast(program)
    raise ValueError(
        f"Unknown target '{target}'. Choose: python, cpp, ast"
    )
