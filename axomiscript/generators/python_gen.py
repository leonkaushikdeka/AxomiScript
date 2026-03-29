# -*- coding: utf-8 -*-
"""
Generate Python 3 source code from an AxomiScript AST.

Design decisions
----------------
* Assamese identifiers are kept as-is (Python 3 accepts Unicode per PEP 3131).
* Assamese string literals are preserved inside double quotes.
* চক্ৰ (loop) → for var in range(start, end + 1):
"""
from __future__ import annotations
from ..core.ast_nodes import (
    ASTNode, Program, VarDecl, PrintStmt, IfStmt,
    LoopStmt, BinOp, Number, StringLiteral, Identifier,
)


def generate(program: Program) -> str:
    """Return indented Python 3 source code for *program*."""
    return "\n".join(_stmt(n, 0) for n in program.body)


def _stmt(node: ASTNode, depth: int) -> str:
    pad = "    " * depth

    if isinstance(node, VarDecl):
        return f"{pad}{node.name} = {_expr(node.value)}"

    if isinstance(node, PrintStmt):
        return f"{pad}print({_expr(node.value)})"

    if isinstance(node, IfStmt):
        lines = [f"{pad}if {_expr(node.condition)}:"]
        lines += [_stmt(s, depth + 1) for s in node.then_body]
        if node.else_body:
            lines.append(f"{pad}else:")
            lines += [_stmt(s, depth + 1) for s in node.else_body]
        return "\n".join(lines)

    if isinstance(node, LoopStmt):
        s, e = _expr(node.start), _expr(node.end)
        lines = [f"{pad}for {node.var} in range({s}, {e} + 1):"]
        lines += [_stmt(n, depth + 1) for n in node.body]
        return "\n".join(lines)

    return f"{pad}# [unsupported: {type(node).__name__}]"


def _expr(node: ASTNode) -> str:
    if isinstance(node, Number):
        return str(node.value) if isinstance(node.value, int) else repr(node.value)
    if isinstance(node, StringLiteral):
        escaped = node.value.replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(node, Identifier):
        return node.name
    if isinstance(node, BinOp):
        return f"({_expr(node.left)} {node.op} {_expr(node.right)})"
    return "None"
