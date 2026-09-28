#!/usr/bin/env python3
"""
Backward Compatibility Proxy
=============================
This file exists so any existing shortcuts or scheduled tasks calling
recolor_ptb_red.py directly continue to function without interruption.
It forwards execution to the current default theme (Green).
"""
import sys
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from apply_theme import apply

if __name__ == "__main__":
    apply("green")
