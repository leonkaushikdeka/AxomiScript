# -*- coding: utf-8 -*-
"""
Compiler error explainer — provides error messages in Assamese.
"""

from __future__ import annotations


ERROR_MESSAGES = {
    "SYNTAX_ERROR": {
        "en": "Syntax Error",
        "as": "ব্যাকৰণ সমস্যা — কোডৰ গঠনত ত্রুটি আছে",
    },
    "UNEXPECTED_TOKEN": {
        "en": "Unexpected token",
        "as": "অপেক্ষা নকৰা চিহ্ন — এই চিহ্নটো এই ঠাইত নাছিল",
    },
    "MISSING_COLON": {
        "en": "Missing colon",
        "as": "কোলন (:) নাই — conditional বা loop শেষ হোৱাৰ পিছত কোলন দিয়ক",
    },
    "MISSING_BRACE": {
        "en": "Missing brace",
        "as": "বন্ধনী ({}) নাই — কোডৰ ব্লক সম্পূর্ণ কৰক",
    },
    "INVALID_NUMBER": {
        "en": "Invalid number",
        "as": "অবৈধ সংখ্যা — সংখ্যাটো সঠিকভাবে লিখক",
    },
    "UNKNOWN_KEYWORD": {
        "en": "Unknown keyword",
        "as": "অজানা keyword — এই শব্দটো বুজি নাপায়",
    },
    "UNDEFINED_VARIABLE": {
        "en": "Undefined variable",
        "as": "অসংজ্ঞায়িত চলক — এই চলকটো আগে ঘোষণা কৰা হোৱা নাই",
    },
    "TYPE_ERROR": {
        "en": "Type error",
        "as": "ধরন সমস্যা — ভুল ধরনৰ মান ব্যৱহাৰ কৰা হৈছে",
    },
}


def explain_error(error_type: str, details: str = "") -> dict:
    """
    Explain a compiler error in Assamese.

    Parameters
    ----------
    error_type : str — error type key (e.g., 'SYNTAX_ERROR')
    details    : str — additional context about the error

    Returns
    -------
    dict with 'en' (English) and 'as' (Assamese) explanations
    """
    msg = ERROR_MESSAGES.get(error_type, ERROR_MESSAGES["SYNTAX_ERROR"])
    result = {
        "en": f"{msg['en']}: {details}" if details else msg["en"],
        "as": f"{msg['as']}" + (f"\nবিৱৰণ: {details}" if details else ""),
    }
    return result


def format_error_line(line_number: int, line: str, error: str) -> str:
    """
    Format an error with line number in both English and Assamese.

    Parameters
    ----------
    line_number : int — line number where error occurred
    line        : str — the source line with error
    error       : str — error type key

    Returns
    -------
    str formatted error message
    """
    exp = explain_error(error)
    return f"""
Line {line_number}: {exp["en"]}
লাইন {line_number}: {exp["as"]}

  {line.strip()}
    """
