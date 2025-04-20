"""
GUI Interface Module

This module provides a graphical user interface for the Markdown exporter.
It includes dialogs for selecting files and configuring export options.
"""

import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Import from our modules
from .path_utils import ensure_str_path, create_export_dir, resolve_path, find_file_in_directory
from .file_operations import read_files_recursive


def create_hidden_root():
    """
    Create and return a hidden Tkinter root window.
    
    Returns:
        tk.Tk: A hidden root window
    """
    root = tk.Tk()
    root.withdraw()
    return root


def select_file():
    """
    Open a file dialog to select a Markdown file.
    
    Returns:
        str or None: Path to the selected file, or None if cancelled
    """
    root = create_hidden_root()
    
    # Show the file dialog
    file_path = filedialog.askopenfilename(
        title="Select Markdown File",
        filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
    )
    
    # Clean up the root window
    root.destroy()
    
    # Return the selected file path or None if cancelled
    return file_path if file_path else None


def get_max_depth():
    """
    Show dialog box to get recursion depth from the user.
    
    Returns:
        int or None: Maximum recursion depth or None for unlimited
    """
    root = create_hidden_root()
    
    # Ask about recursion depth
    max_depth = simpledialog.askinteger(
        title="Recursion Depth",
        prompt="Enter maximum recursion depth (leave empty for unlimited):\n\n"
               "0: Only the main file\n"
               "1: Main file and directly linked files\n"
               "2+: Follow links to the specified depth\n",
        minvalue=0
    )
    
    # Clean up the root window
    root.destroy()
    
    return max_depth


def count_expected_links(file_path, visited=None, current_depth=0, max_depth=None):
    """
    Count the number of unique markdown links in the file and its linked files up to max_depth.
    
    Args:
        file_path (str): Path to the markdown file
        visited (set, optional): Set of already visited files. Defaults to None.
        current_depth (int, optional): Current recursion depth. Defaults to 0.
        max_depth (int, optional): Maximum recursion depth. Defaults to None (unlimited).
        
    Returns:
        tuple: (count, visited_set) - Number of unique links and set of visited files
    """
    # Initialize visited set if not provided
    if visited is None:
        visited = set()
    
    # Add current file to visited set - normalize path to handle path differences
    file_path = os.path.normpath(ensure_str_path(file_path))
    
    # If file has already been visited, don't count it again
    if file_path in visited:
        return 0, visited
        
    # Add file to visited set
    visited.add(file_path)
    
    # Initialize count (includes the current file)
    count = 1  # Start with 1 for the current file
    
    # If we're at max depth, don't process links further
    if max_depth is not None and current_depth >= max_depth:
        return count, visited
    
    # Regular expressions to find markdown links and image links
    md_link_pattern = re.compile(r"(?<!!)\[\[([^\]]*)\]\]")
    img_link_pattern = re.compile(r"!\[\[([^\]]*)\]\]")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find all markdown links
            md_matches = md_link_pattern.findall(content)
            img_matches = img_link_pattern.findall(content)
            
            # Process markdown links (for documents)
            for match in md_matches:
                # Get file path portion (ignoring anchors and aliases)
                file_only = match.split("#")[0].split("|")[0]
                
                # Add .md extension if needed
                if not file_only.endswith('.md') and file_only:
                    file_only = file_only + '.md'
                
                # Skip empty file names
                if not file_only:
                    continue
                
                # Get absolute path to the linked file
                original_dir = os.path.dirname(os.path.abspath(file_path))
                
                # Find the file using our helper function
                linked_file_path = find_file_in_directory(file_only, original_dir)
                file_found = linked_file_path is not None
                
                # Check if file exists and hasn't been visited yet
                if file_found and linked_file_path not in visited:
                    # Get count from recursive call (add to total)
                    sub_count, visited = count_expected_links(
                        linked_file_path, 
                        visited, 
                        current_depth + 1, 
                        max_depth
                    )
                    count += sub_count
            
            # Process image links (for assets)
            for match in img_matches:
                file_only = match.split("#")[0].split("|")[0]
                
                # Skip empty file names
                if not file_only:
                    continue
                    
                original_dir = os.path.dirname(os.path.abspath(file_path))
                
                # Find the file using our helper function
                linked_file_path = find_file_in_directory(file_only, original_dir)
                file_found = linked_file_path is not None
                
                # Check if file exists and hasn't been visited yet
                if file_found and linked_file_path not in visited:
                    visited.add(linked_file_path)
                    count += 1
    except Exception as e:
        print(f"Error counting links in {file_path}: {e}")
    
    return count, visited


def run_export(file_path, max_depth=None):
    """
    Run the export process with the given options.
    
    Args:
        file_path (str): Path to the Markdown file to export
        max_depth (int, optional): Maximum recursion depth. Defaults to None (unlimited).
        
    Returns:
        bool: True if export was successful, False otherwise
    """
    # Resolve the file path
    file_to_export, error = resolve_path(file_path)
    
    if error:
        # Show error message
        root = create_hidden_root()
        messagebox.showerror("Error", error)
        root.destroy()
        return False

    # Count expected links before export
    print(f"Counting expected links for: {file_to_export}")
    expected_count, visited_files = count_expected_links(file_to_export, max_depth=max_depth)
    print(f"Expected file count: {expected_count}")
    print(f"Files that should be included: {[os.path.basename(f) for f in visited_files]}")

    # Create export directory
    export_dir = create_export_dir(file_path)
    
    # Show info about export location
    root = create_hidden_root()
    messagebox.showinfo(
        "Export Location",
        f"Files will be exported to:\n{export_dir}\nExpected file count: {expected_count}"
    )
    root.destroy()
    
    # Clean up existing export directory if it exists
    if os.path.exists(export_dir) and os.path.isdir(export_dir):
        shutil.rmtree(export_dir)
        os.makedirs(export_dir, exist_ok=True)
        os.makedirs(os.path.join(export_dir, "notes"), exist_ok=True)

    # Copy the main file with its original name
    dest_file = os.path.join(export_dir, "notes", os.path.basename(file_to_export))
    shutil.copyfile(file_to_export, dest_file)
    
    # Keep track of copied files
    files_copied = [ensure_str_path(file_to_export)]

    # Process the main file and its linked files
    print(f"Starting file processing with max_depth={max_depth}...")
    read_files_recursive(
        file_to_export, 
        max_depth=max_depth,
        export_dir=export_dir, 
        files_already_copied=files_copied
    )
    
    print(f"Completed file processing. Files copied: {len(files_copied)}")
    print(f"Files copied: {[os.path.basename(f) for f in files_copied]}")
    
    # Compare expected vs actual file count
    actual_count = len(files_copied)
    
    # Count distinct file types
    md_files = sum(1 for f in files_copied if f.lower().endswith('.md'))
    image_files = sum(1 for f in files_copied if any(f.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']))
    other_files = actual_count - md_files - image_files
    
    completion_message = (
        f"Files have been exported to:\n{export_dir}\n\n"
        f"File Count Summary:\n"
        f"Expected: {expected_count}\n"
        f"Actual: {actual_count}\n\n"
        f"Breakdown:\n"
        f"Markdown files: {md_files}\n"
        f"Image files: {image_files}\n"
        f"Other files: {other_files}"
    )
    
    if expected_count > actual_count:
        completion_message += f"\n\n⚠️ {expected_count - actual_count} files may be missing!"
    elif expected_count < actual_count:
        completion_message += f"\n\n⚠️ {actual_count - expected_count} additional files were copied!"
    else:
        completion_message += "\n\n✓ All expected files were copied successfully!"
    
    # Show completion message
    root = create_hidden_root()
    messagebox.showinfo("Export Complete", completion_message)
    root.destroy()
    
    return True


def main():
    """
    Main entry point for the GUI interface.
    """
    # Select a file
    file_path = select_file()
    if not file_path:
        print("No file selected. Exiting.")
        return
    
    # Get recursion depth
    max_depth = get_max_depth()
    
    # Run the export
    run_export(file_path, max_depth)


if __name__ == "__main__":
    main() 