# -*- coding: utf-8 -*-
"""
High-level pipeline: source → AST → Python + C++.
"""

from __future__ import annotations
from .core.ast_nodes import Program
from .core.utils import pretty_ast
from .languages import get_parser
from .generators import python_gen, cpp_gen
from .explainer import explain_error, format_error_line


class CompilationError(Exception):
    """Raised when compilation fails."""

    def __init__(self, error_type: str, line_number: int = 0, line: str = "", details: str = ""):
        self.error_type = error_type
        self.line_number = line_number
        self.line = line
        self.details = details
        self.explanation = explain_error(error_type, details)
        super().__init__(self.explanation["as"])


def run(
    source: str,
    language: str = "assamese",
    verbose: bool = True,
) -> dict:
    """
    Execute the full AxomiScript compilation pipeline.

    Parameters
    ----------
    source   : str   — source code in the specified natural language.
    language : str   — registered language name (default: 'assamese').
    verbose  : bool  — print intermediate stages to stdout.

    Returns
    -------
    dict with keys:
        source, ast, python_code, cpp_code, error

    If compilation fails, 'error' key contains:
        { 'type': str, 'line': int, 'message': { 'en': str, 'as': str } }
    """
    SEP = "─" * 62
    HEAD = "═" * 62

    def hdr(title):
        if verbose:
            print(f"\n{SEP}\n  {title}\n{SEP}")

    if verbose:
        print(f"\n{HEAD}")
        print(f"  AxomiScript — Compilation Pipeline  [{language}]")
        print(HEAD)

    hdr("STEP 1 │ SOURCE CODE  (Input)")
    if verbose:
        print(source, end="")

    hdr("STEP 2 │ ABSTRACT SYNTAX TREE")
    parse = get_parser(language)
    try:
        ast: Program = parse(source)
    except Exception as e:
        lines = source.split("\n")
        return _handle_error(e, lines, verbose)

    if verbose:
        print(pretty_ast(ast))

    hdr("STEP 3 │ GENERATED Python 3")
    py_code = python_gen.generate(ast)
    if verbose:
        print(py_code)

    hdr("STEP 4 │ GENERATED C++17")
    cpp_code = cpp_gen.generate(ast)
    if verbose:
        print(cpp_code)

    if verbose:
        print(f"\n{HEAD}")
        print("  Pipeline complete  ✓")
        print(HEAD + "\n")

    return {
        "source": source,
        "ast": ast,
        "python_code": py_code,
        "cpp_code": cpp_code,
        "error": None,
    }


def _handle_error(exception: Exception, lines: list, verbose: bool) -> dict:
    """Handle compilation errors with Assamese explanations."""
    error_msg = str(exception)

    error_type = "SYNTAX_ERROR"
    line_number = 0
    line_content = ""
    details = error_msg

    if hasattr(exception, "line") and exception.line is not None:
        line_number = exception.line
    if hasattr(exception, "token") and exception.token is not None:
        details = f"'{exception.token}' - অপেক্ষা নকৰা চিহ্ন"
        error_type = "UNEXPECTED_TOKEN"

    if line_number > 0 and line_number <= len(lines):
        line_content = lines[line_number - 1]

    explanation = explain_error(error_type, details)

    if verbose:
        print(format_error_line(line_number, line_content, error_type))
        print(f"\nEnglish: {explanation['en']}")
        print(f"Assamese: {explanation['as']}")

    return {
        "source": "\n".join(lines),
        "ast": None,
        "python_code": None,
        "cpp_code": None,
        "error": {
            "type": error_type,
            "line": line_number,
            "message": explanation,
        },
    }
