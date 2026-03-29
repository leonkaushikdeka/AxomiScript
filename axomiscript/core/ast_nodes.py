# -*- coding: utf-8 -*-
"""
Language-agnostic AST node definitions.
Every supported natural-language frontend compiles to these nodes.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Union


@dataclass
class ASTNode:
    """Abstract base — every AST node inherits from this."""


@dataclass
class Program(ASTNode):
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class VarDecl(ASTNode):
    name:  str
    value: ASTNode


@dataclass
class PrintStmt(ASTNode):
    value: ASTNode


@dataclass
class IfStmt(ASTNode):
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: List[ASTNode] = field(default_factory=list)


@dataclass
class LoopStmt(ASTNode):
    var:   str
    start: ASTNode
    end:   ASTNode
    body:  List[ASTNode]


@dataclass
class BinOp(ASTNode):
    op:    str
    left:  ASTNode
    right: ASTNode


@dataclass
class Number(ASTNode):
    value: Union[int, float]


@dataclass
class StringLiteral(ASTNode):
    value: str  # stored WITHOUT surrounding quotes


@dataclass
class Identifier(ASTNode):
    name: str
