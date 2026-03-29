# -*- coding: utf-8 -*-
"""Utilities for inspecting / serialising the AST."""
from __future__ import annotations
import json
from .ast_nodes import (
    ASTNode, Program, VarDecl, PrintStmt, IfStmt,
    LoopStmt, BinOp, Number, StringLiteral, Identifier,
)


def ast_to_dict(node: ASTNode) -> dict:
    """Recursively convert an AST node to a JSON-serialisable dict."""
    if isinstance(node, Program):
        return {"type": "Program", "body": [ast_to_dict(n) for n in node.body]}
    if isinstance(node, VarDecl):
        return {"type": "VarDecl", "name": node.name, "value": ast_to_dict(node.value)}
    if isinstance(node, PrintStmt):
        return {"type": "PrintStmt", "value": ast_to_dict(node.value)}
    if isinstance(node, IfStmt):
        return {
            "type": "IfStmt",
            "condition": ast_to_dict(node.condition),
            "then": [ast_to_dict(n) for n in node.then_body],
            "else": [ast_to_dict(n) for n in node.else_body],
        }
    if isinstance(node, LoopStmt):
        return {
            "type": "LoopStmt",
            "var": node.var,
            "start": ast_to_dict(node.start),
            "end": ast_to_dict(node.end),
            "body": [ast_to_dict(n) for n in node.body],
        }
    if isinstance(node, BinOp):
        return {"type": "BinOp", "op": node.op,
                "left": ast_to_dict(node.left), "right": ast_to_dict(node.right)}
    if isinstance(node, Number):
        return {"type": "Number", "value": node.value}
    if isinstance(node, StringLiteral):
        return {"type": "String", "value": node.value}
    if isinstance(node, Identifier):
        return {"type": "Identifier", "name": node.name}
    return {"type": "Unknown", "repr": repr(node)}


def pretty_ast(node: ASTNode) -> str:
    """Pretty-printed JSON representation of the AST."""
    return json.dumps(ast_to_dict(node), ensure_ascii=False, indent=2)
