# -*- coding: utf-8 -*-
"""
Language plugin registry.

To add a new language:
  1. Create axomiscript/languages/<name>/__init__.py that exposes `parse`.
  2. Register it here.
"""

from __future__ import annotations
from typing import Dict, Callable
from ..core.ast_nodes import Program

_REGISTRY: Dict[str, Callable[[str], Program]] = {}


def register(name: str, parse_fn: Callable[[str], Program]) -> None:
    """Register a language parser under `name`."""
    _REGISTRY[name] = parse_fn


def get_parser(name: str) -> Callable[[str], Program]:
    if name not in _REGISTRY:
        raise KeyError(f"Language '{name}' is not registered. Available: {list(_REGISTRY)}")
    return _REGISTRY[name]


def available() -> list:
    return list(_REGISTRY)


# ── Auto-register bundled languages ─────────────────────────────────────
from .assamese import parse as _assamese_parse  # noqa: E402

register("assamese", _assamese_parse)
