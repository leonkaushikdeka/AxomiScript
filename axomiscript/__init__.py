# -*- coding: utf-8 -*-
"""
AxomiScript — write, compile, and run natural-language code.

Quick start
-----------
    from axomiscript import compile_source, run_source

    # Compile to Python
    py = compile_source("চলক ক = ১০\\nমুদ্ৰণ ক\\n")
    print(py)

    # Run directly
    result = run_source("মুদ্ৰণ \\"নমস্কাৰ\\"\\n")
    print(result["stdout"])

    # Launch web IDE
    # $ axomiscript serve
"""

from .compiler import compile_source
from .executor import run_source
from .languages import get_parser, available, register
from .core.utils import pretty_ast, ast_to_dict
from .pipeline import run, CompilationError
from .explainer import explain_error, format_error_line

__all__ = [
    "compile_source",
    "run_source",
    "run",
    "CompilationError",
    "explain_error",
    "format_error_line",
    "get_parser",
    "available",
    "register",
    "pretty_ast",
    "ast_to_dict",
]
__version__ = "1.0.0"
