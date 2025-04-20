# Obsidian Recursive Notes Exporter

This document provides a comprehensive overview of the project structure, modules, classes, and functions.

## Project Structure

```
ObsidianRecursiveNotes/
├── __init__.py                      # Package initialization
├── obsidian_recursive_notes/        # Main package directory
│   ├── __init__.py                  # Package initialization
│   ├── main.py                      # Main script entry point
│   ├── path_utils.py                # Path handling utilities 
│   ├── file_operations.py           # File operations (copying, finding files)
│   └── gui_interface.py             # GUI interface
├── requirements.txt                 # Project dependencies
├── test_gui_interface.py            # Test suite for GUI
├── test_file_counting.py            # Test suite for file counting
├── run.py                           # Python launcher
├── run.sh                           # Shell script launcher
├── run_gui.bat                      # Windows batch launcher
├── index.md                         # This file - documentation
└── README.md                        # Project overview and usage
```

## Modules and Functions

### `obsidian_recursive_notes/main.py`

The main entry point for the application, containing the command-line interface and top-level logic.

- **Functions**:
  - `print_usage()` - Print usage instructions for the script
  - `main()` - Main entry point that orchestrates the entire process

### `obsidian_recursive_notes/path_utils.py`

Utility functions for path handling and manipulation.

- **Functions**:
  - `ensure_str_path(path)` - Convert any path object to a string
  - `sanitize_filename(filename)` - Convert a filename to a safe format
  - `find_file_in_directory(filename, base_directory)` - Find a file by name in directories
  - `resolve_path(file_path)` - Resolve a file path, handling both relative and absolute paths
  - `create_export_dir(file_path, base_dir=None)` - Create an export directory structure

### `obsidian_recursive_notes/file_operations.py`

Functions for file operations, including finding, copying, and processing files.

- **Functions**:
  - `copy_file_to_export(file_to_find, current_file, ...)` - Copy a file to the export directory
  - `find_markdown_links(line, current_file, ...)` - Find and process Markdown links
  - `find_image_links(line, current_file, ...)` - Find and process image links
  - `read_files_recursive(path, ...)` - Recursively process markdown files

### `obsidian_recursive_notes/gui_interface.py`

A graphical user interface for the application.

- **Functions**:
  - `create_hidden_root()` - Create and hide a Tkinter root window
  - `select_file()` - Open a file dialog to select a Markdown file
  - `get_max_depth()` - Show dialog to get recursion depth
  - `count_expected_links(file_path, ...)` - Count links in a file recursively
  - `run_export(file_path, max_depth)` - Run the export process
  - `main()` - Main entry point for the GUI

### `run.py`, `run.sh`, and `run_gui.bat`

Launcher scripts that run the GUI interface.

- **Features**:
  - Cross-platform compatibility (Windows, macOS, Linux)
  - Automatically detects Python 3
  - Activates virtual environment if present
  - Launches the GUI interface

## Workflow

1. **User Invocation**: User runs one of the launcher scripts or `main.py` with a markdown file and optional parameters.
2. **Argument Parsing**: `main.py` parses the arguments and sets up the export options.
3. **Path Resolution**: `path_utils.py` resolves the input file path and creates the export directory.
4. **Recursive Processing**: `file_operations.py` recursively processes the markdown file and its links.
5. **File Export**: All linked files are copied to the export directory, preserving their connections.

## Key Features

1. **Recursion Depth Control**: The script can limit how deep it traverses link references.
2. **Circular Reference Handling**: The script detects and handles circular references to prevent infinite loops.
3. **Flattened Structure**: Output files are organized in a flat directory structure for easy access.
4. **Filename Sanitization**: Filenames are sanitized to ensure compatibility across systems.
5. **Detailed Export Summary**: After export, a breakdown of exported files is shown.

## Markdown Features Supported

The script processes these Markdown elements:

- Wiki-style links (`[[link]]`)
- Image links (`![[image.png]]`)
- Links with anchors (`[[link#section]]`)
- Links with aliases (`[[link|alias]]`)
- Self-referential links (`[[]]`) 