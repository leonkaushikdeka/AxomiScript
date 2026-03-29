# -*- coding: utf-8 -*-
"""
Generate C++17 source code from an AxomiScript AST.

Design decisions
----------------
* Every statement ends with a semicolon.
* Assamese string literals use u8"…" — C++17 guarantees UTF-8 encoding.
* Variable types are heuristically inferred: int / double / std::string / auto.
* চক্ৰ (loop) → for (int var = start; var <= end; ++var)
"""
from __future__ import annotations
from ..core.ast_nodes import (
    ASTNode, Program, VarDecl, PrintStmt, IfStmt,
    LoopStmt, BinOp, Number, StringLiteral, Identifier,
)


def generate(program: Program) -> str:
    """Return valid C++17 source code for *program*."""
    lines = [
        "#include <iostream>",
        "#include <string>",
        "",
        "int main() {",
    ]
    sym: dict = {}  # symbol table: name → C++ type string
    for node in program.body:
        lines.extend(_stmt(node, 1, sym))
    lines += ["    return 0;", "}"]
    return "\n".join(lines)


def _stmt(node: ASTNode, depth: int, sym: dict) -> list:
    pad, out = "    " * depth, []

    if isinstance(node, VarDecl):
        ctype = _infer(node.value, sym)
        sym[node.name] = ctype
        out.append(f"{pad}{ctype} {node.name} = {_expr(node.value, sym)};")

    elif isinstance(node, PrintStmt):
        out.append(f"{pad}std::cout << {_expr(node.value, sym)} << std::endl;")

    elif isinstance(node, IfStmt):
        out.append(f"{pad}if ({_expr(node.condition, sym)}) {{")
        for s in node.then_body:
            out.extend(_stmt(s, depth + 1, sym))
        if node.else_body:
            out.append(f"{pad}}} else {{")
            for s in node.else_body:
                out.extend(_stmt(s, depth + 1, sym))
        out.append(f"{pad}}}")

    elif isinstance(node, LoopStmt):
        s = _expr(node.start, sym)
        e = _expr(node.end, sym)
        sym[node.var] = "int"
        out.append(
            f"{pad}for (int {node.var} = {s}; "
            f"{node.var} <= {e}; ++{node.var}) {{"
        )
        for n in node.body:
            out.extend(_stmt(n, depth + 1, sym))
        out.append(f"{pad}}}")

    else:
        out.append(f"{pad}// [unsupported: {type(node).__name__}]")

    return out


def _expr(node: ASTNode, sym: dict) -> str:
    if isinstance(node, Number):
        return str(node.value) if isinstance(node.value, int) else repr(node.value)
    if isinstance(node, StringLiteral):
        escaped = node.value.replace('"', '\\"')
        return f'u8"{escaped}"'
    if isinstance(node, Identifier):
        return node.name
    if isinstance(node, BinOp):
        return (f"({_expr(node.left, sym)} {node.op} "
                f"{_expr(node.right, sym)})")
    return "0"


def _infer(node: ASTNode, sym: dict) -> str:
    """Heuristic C++ type inference: int < double < std::string < auto."""
    if isinstance(node, Number):        return "double" if isinstance(node.value, float) else "int"
    if isinstance(node, StringLiteral): return "std::string"
    if isinstance(node, Identifier):    return sym.get(node.name, "auto")
    if isinstance(node, BinOp):
        lt, rt = _infer(node.left, sym), _infer(node.right, sym)
        if "double"      in (lt, rt): return "double"
        if "std::string" in (lt, rt): return "std::string"
        return "int"
    return "auto"
