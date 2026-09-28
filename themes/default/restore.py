#!/usr/bin/env python3
"""Restore Original Default Blue Theme to DiscordPTB"""
import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from apply_theme import apply

if __name__ == "__main__":
    apply("default")
