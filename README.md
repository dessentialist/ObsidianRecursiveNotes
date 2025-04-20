# Obsidian Recursive Notes Exporter

A powerful tool to export Obsidian notes and their linked files, preserving the network of connections.

![License](https://img.shields.io/github/license/darpan/obsidian-recursive-notes)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)

## Features

- **Recursive Export**: Automatically finds and exports all linked Markdown files and images
- **Customizable Depth**: Control how deeply to follow nested links (from just the main file to unlimited depth)
- **Circular Reference Handling**: Intelligently handles circular references between files
- **Easy GUI Interface**: Simple graphical interface for those who prefer not to use the command line
- **Accurate File Counts**: Shows you exactly how many files will be exported

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/darpan/ObsidianRecursiveNotes.git
   cd ObsidianRecursiveNotes
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### GUI Interface

The simplest way to use the exporter is through its graphical interface:

```
python run.py
```

This will open a file selection dialog, followed by export options.

### Command Line

For advanced users or automation, you can use the command line interface:

```
python -m obsidian_recursive_notes.main path/to/your/file.md [depth]
```

Arguments:
- `path/to/your/file.md`: The path to the Markdown file to export
- `depth`: (Optional) Maximum recursion depth (integer or leave blank for unlimited)

### Examples

1. Export a file with all linked files:
   ```
   python -m obsidian_recursive_notes.main my_notes.md
   ```

2. Export only the specified file and directly linked files (depth 1):
   ```
   python -m obsidian_recursive_notes.main my_notes.md 1
   ```

3. Export a file with linked files up to 3 levels deep:
   ```
   python -m obsidian_recursive_notes.main my_notes.md 3
   ```

## Output Structure

The exported files are organized in a clean structure:

```
export/
└── notes/                  # All exported Markdown and image files
    ├── your_file.md        # Your original Markdown file
    ├── linked_file.md      # Files linked from your original file
    └── images/             # All referenced images
```

## Testing

Run the test suite to verify everything is working correctly:

```
python test_file_counting.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Obsidian](https://obsidian.md/) for creating an amazing knowledge management tool
- All contributors who have helped improve this tool

