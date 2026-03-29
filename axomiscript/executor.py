# -*- coding: utf-8 -*-
"""
Execute compiled AxomiScript programs.

The executor transpiles source to Python, then runs it in a subprocess with
captured stdout/stderr so the output can be displayed in the CLI or web IDE.
"""
from __future__ import annotations
import subprocess
import sys
import tempfile
import os
from .languages import get_parser
from .generators import python_gen


def run_source(source: str, language: str = "assamese", timeout: int = 10) -> dict:
    """
    Transpile *source* to Python and execute it.

    Returns
    -------
    dict with keys:
        stdout  : str   — captured standard output
        stderr  : str   — captured standard error / exception message
        exit_code : int — 0 on success
        python_code : str — the generated Python source
    """
    parse = get_parser(language)
    program = parse(source)
    py_code = python_gen.generate(program)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", encoding="utf-8", delete=False
    ) as f:
        f.write(py_code)
        tmp_path = f.name

    # Force UTF-8 I/O in the child process (needed on Windows where the
    # default console encoding is cp1252 / similar).
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
            env=env,
        )
        return {
            "stdout":      result.stdout,
            "stderr":      result.stderr,
            "exit_code":   result.returncode,
            "python_code": py_code,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout":      "",
            "stderr":      f"Execution timed out after {timeout}s.",
            "exit_code":   -1,
            "python_code": py_code,
        }
    finally:
        os.unlink(tmp_path)
