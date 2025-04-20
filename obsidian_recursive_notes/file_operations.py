"""
File Operations Module

This module provides functions for file operations in the Markdown export process.
Functions include finding and copying files, processing markdown links, and handling recursion.
"""

import os
import re
import shutil
from pathlib import Path

from .path_utils import ensure_str_path, find_file_in_directory


def copy_file_to_export(file_to_find, current_file, traverse=False, export_dir=None, 
                       files_already_copied=None, max_depth=None):
    """
    Copy a file to the export directory and optionally process its links recursively.
    
    Args:
        file_to_find (str): The filename to find and copy
        current_file (str): The current file being processed
        traverse (bool, optional): Whether to recursively process the file. Defaults to False.
        export_dir (str, optional): Export directory path. Defaults to None.
        files_already_copied (list, optional): List of already copied files. Defaults to None.
        max_depth (int, optional): Maximum recursion depth. Defaults to None.
        
    Returns:
        str or None: The basename of the copied file or None if not found
    """
    # Normalize paths for consistency
    current_file = os.path.normpath(ensure_str_path(current_file))
    
    # Check recursion depth limit - if max_depth is 0, we should still copy this file
    # but not process it further
    if max_depth is not None and max_depth < 0:
        return None
    
    # If file_to_find is empty, return None
    if not file_to_find or file_to_find.strip() == "":
        return None
        
    # Set default export directory if none provided
    if export_dir is None:
        export_dir = os.path.join(os.path.expanduser("~/Desktop"), "export")
    
    # Initialize the list of already copied files if none provided
    if files_already_copied is None:
        files_already_copied = []
    
    # Get the directory of the original file
    original_dir = os.path.dirname(os.path.abspath(current_file))
    
    # Find the file using our helper function
    linked_file_path = find_file_in_directory(file_to_find, original_dir)
    
    if linked_file_path:
        # Create notes directory if it doesn't exist
        notes_dir = os.path.join(export_dir, "notes")
        os.makedirs(notes_dir, exist_ok=True)
        
        # Preserve original filename
        dest_file = os.path.join(notes_dir, os.path.basename(linked_file_path))
        shutil.copyfile(linked_file_path, dest_file)
        
        # Normalize linked file path for consistency in comparisons
        linked_file_path = os.path.normpath(linked_file_path)
        
        # Add file to copied list if not already there
        if linked_file_path not in files_already_copied:
            files_already_copied.append(ensure_str_path(linked_file_path))
            
        # Only traverse if requested AND we have remaining depth AND not already traversed (prevents circular references)
        if traverse and linked_file_path not in [os.path.normpath(f) for i, f in enumerate(files_already_copied) if i < len(files_already_copied) - 1]:
            
            # When traversing to the next level, decrement max_depth
            next_depth = None if max_depth is None else max_depth - 1
            
            # Only recurse if we have depth remaining
            if next_depth is None or next_depth >= 0:
                read_files_recursive(
                    linked_file_path, 
                    max_depth=next_depth, 
                    export_dir=export_dir, 
                    files_already_copied=files_already_copied
                )
        
        return os.path.basename(linked_file_path)
    else:
        print(f"Warning: Could not find linked file: {file_to_find}")
        return None


def find_markdown_links(line, current_file, export_dir=None, 
                       files_already_copied=None, max_depth=None):
    """
    Find and process Markdown-style links in the given line.
    
    Args:
        line (str): The line of text to process
        current_file (str): The current file being processed
        export_dir (str, optional): Export directory path. Defaults to None.
        files_already_copied (list, optional): List of already copied files. Defaults to None.
        max_depth (int, optional): Maximum recursion depth. Defaults to None.
        
    Returns:
        str: The processed line with links handled
    """
    # Don't process links if we've reached max depth
    if max_depth is not None and max_depth <= 0:
        return line
    
    pattern = re.compile(r"(?<!!)\[\[([^\]]*)\]\]")
    for file_link in re.findall(pattern, line):
        file_only = file_link.split("#")[0].split("|")[0]
        
        # Handle anchor links
        if len(file_link.split("#")) > 1:
            # Just handling the file part, ignoring anchors for file copy operation
            pass
        
        # Handle self-referential links
        if file_only == "":
            file_only = Path(current_file).name.replace(".md", "")
        else:
            # Add .md extension if needed
            if not file_only.endswith('.md') and file_only:
                file_only = file_only + '.md'
            
            # Skip empty file names
            if not file_only:
                continue
                
            # Set traverse to True only if we can go deeper (max_depth > 1 or None)
            should_traverse = max_depth is None or max_depth > 1
            
            # Try to make output more readable by only printing when something new is found
            if files_already_copied is not None and not any(file_only in f for f in files_already_copied):
                print(f"Processing link: {file_only} from {Path(current_file).name}")
                
            copy_file_to_export(
                file_only, 
                current_file, 
                traverse=should_traverse, 
                export_dir=export_dir, 
                files_already_copied=files_already_copied, 
                max_depth=max_depth
            )
    
    return line


def find_image_links(line, current_file, export_dir=None, files_already_copied=None):
    """
    Find and process image links in the given line.
    
    Args:
        line (str): The line of text to process
        current_file (str): The current file being processed
        export_dir (str, optional): Export directory path. Defaults to None.
        files_already_copied (list, optional): List of files already copied. Used for tracking.
        
    Returns:
        tuple: (processed_line, count_of_images_found)
    """
    pattern = re.compile(r"!\[\[([^\]]*)\]\]")
    assets_count = 0
    
    for file_link in re.findall(pattern, line):
        file_only = file_link.split("#")[0].split("|")[0]
        
        # Skip empty file names
        if not file_only:
            continue
            
        # Handle self-referential links
        if file_only == "":
            file_only = Path(current_file).name.replace(".md", "")
        else:
            # Try to make output more readable by only printing when something new is found
            if files_already_copied is not None and not any(file_only in f for f in files_already_copied):
                print(f"Processing image: {file_only} from {Path(current_file).name}")
                
            copy_file_to_export(
                file_only, 
                current_file, 
                traverse=False,
                export_dir=export_dir,
                files_already_copied=files_already_copied
            )
        
        assets_count += 1
    
    return (line, assets_count)


def read_files_recursive(path, max_depth=None, export_dir=None, files_already_copied=None):
    """
    Recursively read and process markdown files, copying them to the export directory.
    
    Args:
        path (str): Path to the markdown file to process
        max_depth (int, optional): Maximum recursion depth. Defaults to None.
        export_dir (str, optional): Export directory path. Defaults to None.
        files_already_copied (list, optional): List of already copied files. Defaults to None.
    """
    # Check recursion depth limit
    if max_depth is not None and max_depth < 0:
        return
    
    # Set default export directory if none provided
    if export_dir is None:
        export_dir = os.path.join(os.path.expanduser("~/Desktop"), "export")
    
    # Initialize the list of already copied files if none provided
    if files_already_copied is None:
        files_already_copied = []
    
    # Create notes directory if it doesn't exist
    notes_dir = os.path.join(export_dir, "notes")
    os.makedirs(notes_dir, exist_ok=True)
    
    # Copy the main file
    dest_file = os.path.join(notes_dir, os.path.basename(path))
    shutil.copyfile(path, dest_file)
    
    # Read the file content
    with open(path, "r", encoding='utf-8') as read_file:
        data = read_file.readlines()
    
    assets_count = 0
    
    # Process links
    for line in data:
        find_markdown_links(
            line, 
            current_file=path, 
            export_dir=export_dir, 
            files_already_copied=files_already_copied, 
            max_depth=max_depth
        )
        
        line, image_count = find_image_links(
            line, 
            current_file=path, 
            export_dir=export_dir,
            files_already_copied=files_already_copied
        )
        
        assets_count += image_count
    
    print(f"Exported: {path}" + (f" ({assets_count} images)" if assets_count > 0 else '')) 