#!/usr/bin/env python3
"""
Cross-platform launcher for Obsidian Recursive Notes Exporter

This script automatically launches the GUI interface.
It works on Windows, macOS, and Linux.
"""

import sys
from obsidian_recursive_notes.gui_interface import main as gui_main

def main():
    """Launch the GUI interface."""
    print("Starting Obsidian Recursive Notes Exporter...")
    gui_main()

if __name__ == "__main__":
    main()
