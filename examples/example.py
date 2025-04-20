#!/usr/bin/env python3
"""
Example script for using Obsidian Recursive Notes Exporter programmatically

This script demonstrates how to use the library's functions directly in your code.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path if running this script directly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the functions you need
from obsidian_recursive_notes.path_utils import create_export_dir, resolve_path
from obsidian_recursive_notes.file_operations import read_files_recursive
from obsidian_recursive_notes.gui_interface import count_expected_links

def export_markdown_file(file_path, export_to_html=True, max_depth=None):
    """
    Export a markdown file and all its links.
    
    Args:
        file_path (str): Path to the markdown file to export
        export_to_html (bool, optional): Whether to export to HTML. Defaults to True.
        max_depth (int, optional): Maximum recursion depth. Defaults to None (unlimited).
        
    Returns:
        str: Path to the export directory
    """
    # Resolve the input file path
    file_to_export, error = resolve_path(file_path)
    
    if error:
        print(f"Error: {error}")
        return None
    
    # Count the expected number of files to be exported
    expected_count, _ = count_expected_links(file_to_export, max_depth=max_depth)
    print(f"Expected to export {expected_count} files.")
    
    # Create an export directory
    export_dir = create_export_dir(file_path)
    print(f"Will export to: {export_dir}")
    
    # Create the notes directory within the export directory
    os.makedirs(os.path.join(export_dir, "notes"), exist_ok=True)
    
    # Keep track of files we've copied
    files_copied = [file_to_export]
    
    # Process the main file and its linked files
    read_files_recursive(
        file_to_export, 
        max_depth=max_depth, 
        export_to_html=export_to_html, 
        export_dir=export_dir, 
        files_already_copied=files_copied
    )
    
    print(f"Exported {len(files_copied)} files to {export_dir}")
    return export_dir

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python example.py path/to/markdown/file.md [html=True/False] [depth=None]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Default parameters
    export_to_html = True
    max_depth = None
    
    # Parse optional arguments
    if len(sys.argv) > 2:
        export_to_html = sys.argv[2].lower() == "true"
    
    if len(sys.argv) > 3 and sys.argv[3].isdigit():
        max_depth = int(sys.argv[3])
    
    # Run the export
    export_markdown_file(file_path, export_to_html, max_depth) 