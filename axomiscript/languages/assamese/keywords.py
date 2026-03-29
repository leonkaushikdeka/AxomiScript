# -*- coding: utf-8 -*-
"""
Assamese keyword → semantic role mapping.

To add a synonym or a related language, copy this file and
replace the Unicode values with the new language's words.
"""

KEYWORDS = {
    "VAR":   "চলক",    # variable declaration
    "IF":    "যদি",     # if
    "ELSE":  "নহলে",    # else
    "LOOP":  "চক্ৰ",    # for / while loop
    "PRINT": "মুদ্ৰণ",   # print / output
    "TO":    "লৈ",      # range-end  (e.g.  ১ লৈ ৫)
}

# Eastern Nagari → ASCII digit mapping (Assamese uses Nagari numerals)
NAGARI_TO_ASCII = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
