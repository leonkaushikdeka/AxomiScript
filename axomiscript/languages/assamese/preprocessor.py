# -*- coding: utf-8 -*-
"""Pre-processing step: normalise Assamese source before parsing."""
from .keywords import NAGARI_TO_ASCII


def preprocess(source: str) -> str:
    """
    Replace Eastern Nagari digit characters (০১২…) with ASCII (012…)
    so the grammar's NUMBER terminal (/[0-9]+/) matches without changes.

    >>> preprocess("চলক ক = ১০")
    'চলক ক = 10'
    """
    return source.translate(NAGARI_TO_ASCII)
