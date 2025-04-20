"""
Path Utilities Module

This module provides utilities for handling file paths in the Markdown export process.
Functions include string conversion, sanitization, and relative path calculation.
"""

import os
import re
from pathlib import Path


def ensure_str_path(path):
    """
    Convert any path object to a string.
    
    Args:
        path: A path object or string to convert
        
    Returns:
        str: The string representation of the path, or None if input is None
    """
    if path is None:
        return None
    return str(path) if not isinstance(path, str) else path


def sanitize_filename(filename):
    """
    Convert a filename to a safe format by removing problematic characters.
    
    Args:
        filename (str): The filename to sanitize
        
    Returns:
        str: A sanitized version of the filename
    """
    # Remove any directory path
    filename = os.path.basename(filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Replace special characters with underscores
    filename = re.sub(r'[^\w\-_.]', '_', filename)
    return filename


def find_rel_path(link_path, current_file):
    """
    Get the relative path for HTML links using a flattened structure.
    
    Args:
        link_path (str): Path to the linked file
        current_file (str): Path to the current file
        
    Returns:
        str: The relative path for the HTML link
    """
    # For our flattened structure, we just need the filename
    return "notes/" + sanitize_filename(os.path.basename(link_path))


def resolve_path(file_path):
    """
    Resolve a file path, handling both relative and absolute paths.
    
    Args:
        file_path (str): The path to resolve
        
    Returns:
        tuple: (resolved_path, error_message) where error_message is None if successful
    """
    # Handle both relative and absolute paths
    if os.path.isabs(file_path):
        # If it's an absolute path, verify it exists
        if os.path.exists(file_path):
            return file_path, None
        else:
            return None, f"Error: File not found at absolute path: {file_path}"
    else:
        # If it's a relative path, convert to absolute
        abs_path = os.path.abspath(file_path)
        if os.path.exists(abs_path):
            return abs_path, None
        else:
            return None, f"Error: File not found: {file_path}"


def create_export_dir(file_path, base_dir=None):
    """
    Create an export directory structure for the given file.
    
    Args:
        file_path (str): Path to the markdown file being exported
        base_dir (str, optional): Base directory for export. Defaults to desktop.
        
    Returns:
        str: Path to the created export directory
    """
    # Get the original filename without extension for the folder name
    original_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Create export directory on desktop or specified base directory
    if base_dir is None:
        base_dir = os.path.expanduser("~/Desktop")
        
    export_dir = os.path.join(base_dir, original_name)
    
    # Create the export directory structure
    os.makedirs(export_dir, exist_ok=True)
    os.makedirs(os.path.join(export_dir, "notes"), exist_ok=True)
    
    return export_dir 