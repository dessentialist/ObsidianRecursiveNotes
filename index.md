# Obsidian Recursive Notes Exporter

This document provides a comprehensive overview of the project structure, modules, classes, and functions.

## Project Structure

```
ObsidianRecursiveNotes/
├── __init__.py                # Package initialization
├── main.py                    # Main script entry point
├── path_utils.py              # Path handling utilities
├── html_converter.py          # Markdown to HTML conversion
├── file_operations.py         # File operations (copying, finding files)
├── requirements.txt           # Project dependencies
├── test_exportMdFileToHtml.py # Test suite
├── index.md                   # This file - documentation
└── README.md                  # Project overview and usage
```

## Modules and Functions

### `main.py`

The main entry point for the application, containing the command-line interface and top-level logic.

- **Functions**:
  - `print_usage()` - Print usage instructions for the script
  - `main()` - Main entry point that orchestrates the entire process

### `path_utils.py`

Utility functions for path handling and manipulation.

- **Functions**:
  - `ensure_str_path(path)` - Convert any path object to a string
  - `sanitize_filename(filename)` - Convert a filename to a safe format
  - `find_rel_path(link_path, current_file)` - Get the relative path for HTML links
  - `resolve_path(file_path)` - Resolve a file path, handling both relative and absolute paths
  - `create_export_dir(file_path, base_dir=None)` - Create an export directory structure

### `html_converter.py`

Functions for converting Markdown elements to HTML.

- **Functions**:
  - `convert_inline_code(line)` - Convert inline code to HTML
  - `convert_code_block(line, in_code_block)` - Convert code blocks to HTML
  - `convert_comment_block(line, in_comment)` - Convert comment blocks to HTML
  - `convert_horizontal_rule(line)` - Convert horizontal rules to HTML
  - `convert_link_in_text(line)` - Convert inline links to HTML
  - `convert_external_links(line)` - Convert external URLs to HTML links
  - `convert_checkboxes(line)` - Convert checkboxes to HTML
  - `convert_bold_text(line)` - Convert bold text to HTML
  - `convert_headings(line)` - Convert headings to HTML
  - `convert_list_items(line)` - Convert list items to HTML
  - `insert_paragraphs(line)` - Insert paragraph tags for empty lines
  - `generate_html_head(title=None)` - Generate the HTML head section
  - `generate_html_body_start(has_sidebar=True)` - Generate the HTML body opening
  - `generate_html_body_end(sidebar_content=None)` - Generate the HTML body closing
  - `generate_index_html(target_file)` - Generate a simple index.html file

### `file_operations.py`

Functions for file operations, including finding, copying, and processing files.

- **Functions**:
  - `copy_file_to_export(file_to_find, current_file, ...)` - Copy a file to the export directory
  - `find_markdown_links(line, current_file, ...)` - Find and process Markdown links
  - `find_image_links(line, current_file, ...)` - Find and process image links
  - `read_files_recursive(path, ...)` - Recursively process markdown files
  - `process_file_to_html(path, data, ...)` - Process a file and convert to HTML
  - `generate_treeview_html(files_list, export_dir)` - Generate a treeview HTML file

### `gui_interface.py`

A graphical user interface for the application.

- **Functions**:
  - `select_file()` - Open a file dialog to select a Markdown file
  - `get_export_options()` - Show dialogs to get export options
  - `run_export(file_path, export_to_html, max_depth)` - Run the export process
  - `main()` - Main entry point for the GUI

### `run.sh`

A shell script that launches the GUI interface.

- **Features**:
  - Automatically detects Python 3
  - Activates virtual environment if present
  - Launches the GUI interface

## Workflow

1. **User Invocation**: User runs `main.py` with a markdown file and optional parameters.
2. **Argument Parsing**: `main.py` parses the arguments and sets up the export options.
3. **Path Resolution**: `path_utils.py` resolves the input file path and creates the export directory.
4. **Recursive Processing**: `file_operations.py` recursively processes the markdown file and its links.
5. **HTML Conversion**: If requested, `html_converter.py` converts markdown to HTML.
6. **Navigation Generation**: A treeview and index file are generated for easy navigation.

## Key Features

1. **Recursion Depth Control**: The script can limit how deep it traverses link references.
2. **Circular Reference Handling**: The script detects and handles circular references to prevent infinite loops.
3. **Flattened Structure**: Output files are organized in a flat directory structure for easy access.
4. **HTML Navigation**: When exporting to HTML, a sidebar is generated for easy navigation between files.
5. **Filename Sanitization**: Filenames are sanitized to ensure compatibility across systems.

## Markdown Features Supported

The script supports conversion of various Markdown elements to HTML:

- Wiki-style links (`[[link]]`)
- Image links (`![[image.png]]`)
- Code blocks (``` ... ```)
- Inline code (`code`)
- Comments (`%% comment %%`)
- Horizontal rules (`---`)
- Links (`[text](url)`)
- External URLs
- Checkboxes (`- [ ]` and `- [x]`)
- Bold text (`**bold**`)
- Headings (`# Heading`)
- Lists (`- item`) 