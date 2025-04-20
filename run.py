#!/usr/bin/env python3
"""
Cross-platform launcher for Obsidian Recursive Notes Exporter

This script automatically launches the GUI interface.
It works on Windows, macOS, and Linux.
"""

import os
import sys
import platform
import subprocess

def main():
    """Launch the GUI interface."""
    print("Starting Obsidian Recursive Notes Exporter...")
    
    try:
        # Import only when needed to avoid issues during setup
        from obsidian_recursive_notes.gui_interface import main as gui_main
        
        # Run the GUI directly
        gui_main()
    except ImportError:
        print("Error importing the Obsidian Recursive Notes package.")
        print("Make sure you have installed the package or are running from the correct directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting the GUI: {e}")
        print("Please check that Python and tkinter are properly installed.")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main() 