"""
File Operations Module

This module provides functions for file operations in the Markdown export process.
Functions include finding and copying files, processing markdown links, and handling recursion.
"""

import os
import re
import shutil
from pathlib import Path
import html

from path_utils import ensure_str_path, find_rel_path, sanitize_filename
import html_converter


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
    linked_file_path = ""
    
    # Try to find the file in the same directory as the original file first
    potential_path = os.path.join(original_dir, file_to_find)
    potential_path = os.path.normpath(potential_path)
    if os.path.exists(potential_path):
        linked_file_path = potential_path
    else:
        # If not found, search recursively in the original directory
        for root, _, files in os.walk(original_dir):
            for file in files:
                if file == file_to_find:
                    linked_file_path = os.path.join(root, file)
                    linked_file_path = os.path.normpath(linked_file_path)
                    break
            if linked_file_path:
                break
    
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
                    export_to_html=False, 
                    export_dir=export_dir, 
                    files_already_copied=files_already_copied
                )
        
        return os.path.basename(linked_file_path)
    else:
        print(f"Warning: Could not find linked file: {file_to_find}")
        return None


def find_markdown_links(line, current_file, export_to_html=False, export_dir=None, 
                       files_already_copied=None, max_depth=None):
    """
    Find and process Markdown-style links in the given line.
    
    Args:
        line (str): The line of text to process
        current_file (str): The current file being processed
        export_to_html (bool, optional): Whether to convert links to HTML format. Defaults to False.
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
        new_file = None
        
        # Handle anchor links
        anchor = ""
        if len(file_link.split("#")) > 1:
            anchor = "#" + file_link.split("#")[1].replace(" ", "_").replace("(", "").replace(")", "")
        
        # Handle self-referential links
        if anchor != "" and file_only == "":
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
                
            new_file = copy_file_to_export(
                file_only, 
                current_file, 
                traverse=should_traverse, 
                export_dir=export_dir, 
                files_already_copied=files_already_copied, 
                max_depth=max_depth
            )
        
        # Replace markdown links with HTML links if exporting to HTML
        if export_to_html:
            if new_file and len(new_file) > 0:
                html_link = f'<a href="./{new_file}.html{anchor}">{new_file.replace("\\","/").split("/")[-1].replace(".md","")}{anchor}</a>'
                line = line.replace(f'[[{file_link}]]', html_link)
            else:  # Self-reference or file not found
                html_link = f'<a href="./{file_only}.md.html{anchor}">{file_only.replace("\\","/").split("/")[-1].replace(".md","")}{anchor}</a>'
                line = line.replace(f'[[{file_link}]]', html_link)
    
    return line


def find_image_links(line, current_file, export_to_html=False, export_dir=None, files_already_copied=None):
    """
    Find and process image links in the given line.
    
    Args:
        line (str): The line of text to process
        current_file (str): The current file being processed
        export_to_html (bool, optional): Whether to convert links to HTML format. Defaults to False.
        export_dir (str, optional): Export directory path. Defaults to None.
        files_already_copied (list, optional): List of files already copied. Used for tracking.
        
    Returns:
        tuple: (processed_line, count_of_images_found)
    """
    pattern = re.compile(r"!\[\[([^\]]*)\]\]")
    assets_count = 0
    
    for file_link in re.findall(pattern, line):
        file_only = file_link.split("#")[0].split("|")[0]
        new_file = None
        
        # Handle anchor links
        anchor = ""
        if len(file_link.split("#")) > 1:
            anchor = "#" + file_link.split("#")[1].replace(" ", "_").replace("(", "").replace(")", "")
        
        # Skip empty file names
        if not file_only:
            continue
            
        # Handle self-referential links
        if anchor != "" and file_only == "":
            file_only = Path(current_file).name.replace(".md", "")
        else:
            # Try to make output more readable by only printing when something new is found
            if files_already_copied is not None and not any(file_only in f for f in files_already_copied):
                print(f"Processing image: {file_only} from {Path(current_file).name}")
                
            new_file = copy_file_to_export(
                file_only, 
                current_file, 
                traverse=False,
                export_dir=export_dir,
                files_already_copied=files_already_copied
            )
        
        # Replace markdown image links with HTML img tags if exporting to HTML
        if export_to_html:
            if new_file and len(new_file) > 0:
                line = line.replace(f'![[{file_link}]]', f'<img src="./{new_file}" alt="{new_file}">')
            else:  # Self-reference or file not found
                line = line.replace(f'![[{file_link}]]', f'<img src="./{file_only}" alt="{file_only}">')
        
        assets_count += 1
    
    return (line, assets_count)


def read_files_recursive(path, max_depth=None, export_to_html=False, export_dir=None, files_already_copied=None):
    """
    Recursively read and process markdown files, copying them to the export directory.
    
    Args:
        path (str): Path to the markdown file to process
        max_depth (int, optional): Maximum recursion depth. Defaults to None.
        export_to_html (bool, optional): Whether to convert to HTML. Defaults to False.
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
    
    # Process the file - either export to HTML or just process the links
    if export_to_html:
        process_file_to_html(path, data, export_dir, files_already_copied, max_depth, assets_count)
    else:
        # Process links without converting to HTML
        for line in data:
            find_markdown_links(
                line, 
                current_file=path, 
                export_to_html=export_to_html, 
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


def process_file_to_html(path, data, export_dir, files_already_copied, max_depth, assets_count):
    """
    Process a markdown file and convert it to HTML.
    
    Args:
        path (str): Path to the file being processed
        data (list): Lines of the file content
        export_dir (str): Export directory path
        files_already_copied (list): List of already copied files
        max_depth (int or None): Maximum recursion depth
        assets_count (int): Counter for assets processed
    """
    output_file_path = os.path.join(export_dir, str(path) + ".html")
    
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Write HTML header
        output_file.write(html_converter.generate_html_head(title=os.path.basename(path)))
        
        # Start HTML body
        output_file.write(html_converter.generate_html_body_start(has_sidebar=True))
        
        # Process content line by line
        in_code_block = False
        in_comment = False
        
        for line in data:
            if not in_code_block:
                line = html_converter.convert_inline_code(line)
            
            line, in_code_block = html_converter.convert_code_block(line, in_code_block)
            
            if not in_code_block:
                if in_comment:
                    line, in_comment = html_converter.convert_comment_block(line, in_comment)
                    line = ''
                else:
                    line, in_comment = html_converter.convert_comment_block(line, in_comment)
                    if in_comment:
                        continue
                    
                    # Process various markdown elements
                    line = html_converter.convert_horizontal_rule(line)
                    line = find_markdown_links(
                        line, 
                        current_file=path, 
                        export_to_html=True, 
                        export_dir=export_dir, 
                        files_already_copied=files_already_copied, 
                        max_depth=max_depth
                    )
                    
                    processed_line, image_count = find_image_links(
                        line, 
                        current_file=path, 
                        export_to_html=True, 
                        export_dir=export_dir,
                        files_already_copied=files_already_copied
                    )
                    line = processed_line
                    assets_count += image_count
                    
                    line = html_converter.convert_inline_code(line)
                    line = html_converter.convert_link_in_text(line)
                    line = html_converter.convert_external_links(line)
                    line = html_converter.convert_checkboxes(line)
                    line = html_converter.convert_bold_text(line)
                    line = html_converter.convert_headings(line)
                    line = html_converter.convert_list_items(line)
                    line = html_converter.insert_paragraphs(line)
            
            elif "<code" not in line:
                line = html.escape(line)
            
            output_file.write(line)
        
        # Sidebar content (iframe with treeview)
        sidebar_content = f'\t<iframe src="{find_rel_path(".", path)[:-1]}treeview.html" width="340px" frameBorder="0" height="900px"></iframe>\n'
        
        # Write HTML footer with sidebar
        output_file.write(html_converter.generate_html_body_end(sidebar_content=sidebar_content))


def generate_treeview_html(files_list, export_dir):
    """
    Generate a treeview HTML file that shows all exported files.
    
    Args:
        files_list (list): List of files that have been exported
        export_dir (str): Path to the export directory
    """
    treeview_path = os.path.join(export_dir, "treeview.html")
    
    with open(treeview_path, 'w') as output_file:
        # HTML header
        output_file.write("<!DOCTYPE html>\n<html>\n<head>\n")
        output_file.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>\n')
        output_file.write('<base target="_parent">\n')
        
        # CSS styles
        output_file.write("<style>\n")
        output_file.write('ul{ padding-left: 5px; margin-left: 15px; list-style-type: "- "; }\n')
        output_file.write(".folderClass {list-style-type: disc;}\n")
        output_file.write("</style>\n")
        output_file.write("</head>\n")
        
        # Body with treeview
        output_file.write('<body style="background: #F0F0F0;">\n')
        
        # Sort files for consistent display
        files_list.sort()
        
        # Start the treeview
        output_file.write("<ul>")
        
        # Process the first file to create the initial tree structure
        if files_list:
            for folder in str(files_list[0]).replace("\\", "/").split("/"):
                if '.md' in folder:
                    output_file.write(f'<li><a href="./{files_list[0]}.html">{folder.replace(".md", "")}</a></li>\n')
                else:
                    output_file.write(f'<li class="folderClass">{folder}</li>\n<ul>')
            
            # Track the path for proper nesting
            last_file_path = str(files_list[0]).replace("\\", "/").split("/")
            
            # Process the rest of the files
            for i, curr_file in enumerate(files_list):
                if i == 0:  # Skip the first one as we've already processed it
                    continue
                
                for curr_folder in str(curr_file).replace("\\", "/").split("/"):
                    if len(last_file_path) > 0 and curr_folder == last_file_path[0]:
                        del last_file_path[0]
                    else:
                        # Close previous lists
                        for _ in last_file_path[:-1]:
                            output_file.write("</ul>\n")
                        
                        last_file_path = ""
                        if '.md' in curr_folder:
                            output_file.write(f'<li><a href="./{curr_file}.html">{curr_folder.replace(".md", "")}</a></li>\n')
                        else:
                            output_file.write(f'<li class="folderClass">{curr_folder}</li>\n<ul>\n')
                
                last_file_path = str(curr_file).replace("\\", "/").split("/")
            
            # Close all remaining open lists
            for _ in str(files_list[-1]).replace("\\", "/").split("/"):
                output_file.write("</ul>")
        
        output_file.write("</body>\n</html>\n") 