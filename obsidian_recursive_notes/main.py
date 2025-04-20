#!/usr/bin/env python3
"""
Obsidian Recursive Notes Exporter

This script exports Obsidian Markdown files to a directory structure,
preserving links between files and images.

Features:
- Recursively processes Markdown links
- Handles both absolute and relative paths
- Supports configurable recursion depth
- Creates a directory structure on the user's desktop

Usage:
  python -m obsidian_recursive_notes.main <filename.md> [depth]
  
  Arguments:
    filename.md    - Path to the Markdown file to export
    [depth]        - (Optional) Maximum recursion depth for linked files
"""

import os
import sys
import shutil

from .path_utils import ensure_str_path, create_export_dir, resolve_path
from .file_operations import read_files_recursive


def print_usage():
    """Print usage instructions for the script."""
    print("Usage: python -m obsidian_recursive_notes.main <filename.md> "
          "[depth](optional, recursion depth for linked files)")


def main():
    """Main entry point for the script."""
    # Check arguments
    if len(sys.argv) not in [2, 3]:
        print("Wrong number of arguments!")
        print_usage()
        sys.exit(1)

    # Get the file to export
    file_to_find = str(sys.argv[1])
    file_to_export, error = resolve_path(file_to_find)
    
    if error:
        print(error)
        sys.exit(1)

    # Process options
    max_depth = None  # Default to unlimited depth

    if len(sys.argv) >= 3:
        try:
            max_depth = int(sys.argv[2])
        except ValueError:
            print("Error: Recursion depth must be an integer")
            sys.exit(1)

    # Create export directory on desktop
    export_dir = create_export_dir(file_to_find)
    print(f"Path to export folder: {export_dir}\n")

    # Clean up existing export directory if it exists
    if os.path.exists(export_dir) and os.path.isdir(export_dir):
        shutil.rmtree(export_dir)
        os.makedirs(export_dir, exist_ok=True)
        os.makedirs(os.path.join(export_dir, "notes"), exist_ok=True)

    # Copy the main file with its original name
    dest_file = os.path.join(export_dir, "notes", os.path.basename(file_to_find))
    shutil.copyfile(file_to_export, dest_file)
    
    # Keep track of copied files
    files_copied = [ensure_str_path(file_to_export)]

    # Process the main file and its linked files
    read_files_recursive(
        file_to_export, 
        max_depth=max_depth, 
        export_dir=export_dir, 
        files_already_copied=files_copied
    )
    
    # Print completion message
    print(f"Done!\n\nPath to export: {export_dir}")


if __name__ == "__main__":
    main() 