# -*- coding: utf-8 -*-
"""
AxomiScript Command-Line Interface.

Subcommands
-----------
  compile   Transpile source to Python or C++
  run       Transpile and execute
  check     Parse and show AST (syntax check)
  repl      Interactive REPL
  serve     Launch the web IDE

Examples
--------
  axomiscript run program.as
  axomiscript compile program.as --to python -o out.py
  axomiscript compile program.as --to cpp -o out.cpp
  axomiscript check program.as
  axomiscript repl
  axomiscript serve --port 5000
"""

from __future__ import annotations
import argparse
import io
import sys
import os

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from .compiler import compile_source
from .executor import run_source
from .languages import available


# ── Subcommand: compile ──────────────────────────────────────────────────


def cmd_compile(args):
    source = _read_source(args.file)
    target = args.to

    try:
        output = compile_source(source, language=args.lang, target=target)
    except Exception as e:
        print(f"Compile error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Written to {args.output}")
    else:
        print(output)


# ── Subcommand: run ──────────────────────────────────────────────────────


def cmd_run(args):
    source = _read_source(args.file)

    try:
        result = run_source(source, language=args.lang, timeout=args.timeout)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if result["stdout"]:
        print(result["stdout"], end="")
    if result["stderr"]:
        print(result["stderr"], file=sys.stderr, end="")
    sys.exit(result["exit_code"])


# ── Subcommand: check ────────────────────────────────────────────────────


def cmd_check(args):
    source = _read_source(args.file)

    try:
        output = compile_source(source, language=args.lang, target="ast")
        print("Syntax OK")
        if args.ast:
            print(output)
    except Exception as e:
        print(f"Syntax error: {e}", file=sys.stderr)
        sys.exit(1)


# ── Subcommand: repl ─────────────────────────────────────────────────────


def cmd_repl(args):
    from .executor import run_source as _run

    print(f"AxomiScript REPL  (language: {args.lang})")
    print("Type code and press Enter twice to run. Ctrl+C or 'exit' to quit.")
    print("─" * 50)

    while True:
        lines = []
        try:
            while True:
                prompt = ">>> " if not lines else "... "
                try:
                    line = input(prompt)
                except EOFError:
                    print()
                    return
                if line.strip() == "exit":
                    return
                lines.append(line)
                # Run on blank line or single-line statements
                if line == "" or (len(lines) == 1 and _is_complete(line)):
                    break
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            continue

        source = "\n".join(lines)
        if not source.strip():
            continue

        try:
            result = _run(source, language=args.lang)
            if result["stdout"]:
                print(result["stdout"], end="")
            if result["stderr"]:
                print("Error:", result["stderr"], file=sys.stderr)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


def _is_complete(line: str) -> bool:
    """A single line is complete if it doesn't start a block."""
    stripped = line.strip()
    return not stripped.endswith("{")


# ── Subcommand: serve ────────────────────────────────────────────────────


def cmd_serve(args):
    try:
        from .web.app import create_app
    except ImportError:
        print("Flask is required for the web IDE. Install it with:")
        print("  pip install axomiscript[web]")
        sys.exit(1)

    app = create_app()
    print(f"AxomiScript IDE → http://localhost:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


# ── Helpers ──────────────────────────────────────────────────────────────


def _read_source(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as f:
        return f.read()


# ── Argument parser ──────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        prog="axomiscript",
        description="AxomiScript — write, compile, and run natural-language code",
    )
    root.add_argument(
        "--lang",
        "-l",
        default="assamese",
        metavar="LANG",
        help=f"Source language (available: {available()})",
    )
    sub = root.add_subparsers(dest="cmd", required=True)

    # compile
    p_compile = sub.add_parser("compile", help="Transpile to Python or C++")
    p_compile.add_argument("file", help="Source file (.as) or - for stdin")
    p_compile.add_argument(
        "--to",
        default="python",
        choices=["python", "cpp", "ast"],
        help="Target language (default: python)",
    )
    p_compile.add_argument(
        "--output", "-o", metavar="FILE", help="Write output to FILE instead of stdout"
    )

    # run
    p_run = sub.add_parser("run", help="Transpile and execute")
    p_run.add_argument("file", help="Source file (.as) or - for stdin")
    p_run.add_argument(
        "--timeout", type=int, default=10, metavar="SECONDS", help="Execution timeout (default: 10)"
    )

    # check
    p_check = sub.add_parser("check", help="Parse and check syntax")
    p_check.add_argument("file", help="Source file (.as) or - for stdin")
    p_check.add_argument("--ast", action="store_true", help="Print the AST on success")

    # repl
    p_repl = sub.add_parser("repl", help="Interactive REPL")
    # (inherits --lang from root)

    # serve
    p_serve = sub.add_parser("serve", help="Launch the web IDE")
    p_serve.add_argument("--port", type=int, default=5000)
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--debug", action="store_true")

    return root


def main():
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "compile": cmd_compile,
        "run": cmd_run,
        "check": cmd_check,
        "repl": cmd_repl,
        "serve": cmd_serve,
    }
    dispatch[args.cmd](args)


if __name__ == "__main__":
    main()
