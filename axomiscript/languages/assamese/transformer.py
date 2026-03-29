# -*- coding: utf-8 -*-
"""Lark Transformer: CST → typed AST nodes."""
from __future__ import annotations
from lark import Transformer
from ...core.ast_nodes import (
    ASTNode, Program, VarDecl, PrintStmt, IfStmt,
    LoopStmt, BinOp, Number, StringLiteral, Identifier,
)


class _ElseClause:
    """Internal sentinel — never appears in the final AST."""
    def __init__(self, body):
        self.body = body


class AssameseTransformer(Transformer):
    """
    Visits every CST node bottom-up and returns the corresponding typed ASTNode.
    Semantic-free tokens (keywords, NEWLINE) return None and are stripped
    by _keep() before parent rules inspect their children.
    """

    @staticmethod
    def _keep(items):
        return [i for i in items if i is not None]

    @staticmethod
    def _fold(items):
        """Left-fold [expr, op, expr, op, ...] → nested BinOp tree."""
        result = items[0]
        i = 1
        while i < len(items):
            result = BinOp(op=str(items[i]), left=result, right=items[i + 1])
            i += 2
        return result

    # ── Statements ──────────────────────────────────────────────────────
    def start(self, items):
        return Program(body=[i for i in items if isinstance(i, ASTNode)])

    def statement(self, items):
        items = self._keep(items)
        return items[0] if items else None

    def var_decl(self, items):
        items = self._keep(items)
        return VarDecl(name=items[0].name, value=items[1])

    def print_stmt(self, items):
        return PrintStmt(value=self._keep(items)[0])

    def if_stmt(self, items):
        items = self._keep(items)
        condition = items[0]
        then_body, else_body = [], []
        for item in items[1:]:
            if isinstance(item, _ElseClause):
                else_body = item.body
            else:
                then_body.append(item)
        return IfStmt(condition=condition, then_body=then_body, else_body=else_body)

    def else_clause(self, items):
        return _ElseClause(body=[i for i in items if isinstance(i, ASTNode)])

    def loop_stmt(self, items):
        items = self._keep(items)
        return LoopStmt(var=items[0].name, start=items[1], end=items[2], body=items[3:])

    # ── Expressions ─────────────────────────────────────────────────────
    def expr(self, items):       return self._keep(items)[0]
    def comparison(self, items): return self._fold(self._keep(items))
    def arith(self, items):      return self._fold(self._keep(items))
    def term(self, items):       return self._fold(self._keep(items))
    def factor(self, items):     return self._keep(items)[0]

    # ── Terminals ───────────────────────────────────────────────────────
    def NUMBER(self, t):
        s = str(t)
        return Number(value=float(s) if "." in s else int(s))

    def STRING(self, t):
        return StringLiteral(value=str(t)[1:-1])   # strip surrounding quotes

    def IDENT(self, t):
        return Identifier(name=str(t))

    def CMP_OP(self, t): return t
    def ADD_OP(self, t): return t
    def MUL_OP(self, t): return t

    # Semantic-free tokens → discard
    def KW_VAR(self, _):   return None
    def KW_IF(self, _):    return None
    def KW_ELSE(self, _):  return None
    def KW_LOOP(self, _):  return None
    def KW_PRINT(self, _): return None
    def KW_TO(self, _):    return None
    def NEWLINE(self, _):  return None
