# Backend Structure Document

This document outlines the backend structure for the Obsidian Recursive Notes Exporter project. Although this is a local Python-based tool rather than a web server architecture, the document provides an overview of how its backend components are organized, maintained, and executed.

## Backend Architecture

The backend is built using Python 3.6+ and follows a modular architecture. Different modules handle discrete responsibilities in order to keep the code organized, maintainable, and scalable. Key points include:

- **Modular Design:** Each module (e.g., file operations, path utilities, GUI interface) is responsible for specific tasks, enabling easy updates and troubleshooting.
- **Design Patterns:** Emphasis is placed on a clean separation of concerns. For example, the recursive file processing is separated from GUI functionality, ensuring that the CLI and GUI components share underlying logic.
- **Single Execution Flow:** The program can be executed via the CLI or GUI. Regardless of the entry point, the internal workflow for handling file operations and recursive data export remains consistent.
- **Scalability and Maintainability:** Although the tool processes local files, its structure supports extending features such as additional export options or further customizations without major refactoring.

## Database Management

No traditional database is used in this project. Instead, the file system serves as the storage and organizational mechanism. Here’s how data is managed:

- **Data Storage:** The exported notes and images are stored in a dedicated directory structure, ensuring that the relationships (links) between files are preserved.
- **Data Organization:** Files are organized in the file system into a clear hierarchy (an export directory with notes and images subdirectories).
- **Data Handling Practices:** Due to the absence of a backend database, management practices focus on:
  - Sanitizing filenames for cross-platform compatibility
  - Graceful error handling during file operations
  - Handling Unicode characters properly

## Database Schema

Since this project does not use a traditional SQL or NoSQL database, data schema details pertain to the directory structure and file layout. The data is stored on the file system in the following manner:

- **Export Directory Structure:**
  - The main export folder contains a subfolder called `notes`.
  - All exported Markdown files are placed inside the `notes` directory.
  - An `images` subdirectory exists inside the `notes` directory for storing all image files.

*Human Readable Schema Overview:*

- Export (Directory)
  - Notes (Directory)
    - Markdown Files (e.g., your_file.md, linked_file.md)
    - Images (Subdirectory containing image files)

## API Design and Endpoints

This project does not expose external APIs since it is a desktop tool designed to be executed locally. However, internal functions serve as APIs between modules. These internal endpoints facilitate the flow of data between components:

- **CLI and GUI Entry Points:**
  - `obsidian_recursive_notes.main`: Main entry for CLI execution.
  - `obsidian_recursive_notes.gui_interface`: Responsible for GUI operations (file selection, gathering user inputs, and initiating export).
- **Internal Function API:**
  - **Path Utilities:** `ensure_str_path()`, `sanitize_filename()`, `resolve_path()`, and `create_export_dir()` are used for uniform path handling.
  - **File Operations:** Functions such as `copy_file_to_export()`, `find_markdown_links()`, `find_image_links()`, and `read_files_recursive()` manage the core logic for recursive file processing and export.

## Hosting Solutions

Given that the Obsidian Recursive Notes Exporter is a locally-run tool, traditional hosting on cloud servers or on-premises environments is not applicable. Key notes include:

- **Local Execution:** The backend is executed directly on the user's machine when the tool is run via CLI or GUI.
- **Packaging and Distribution:**
  - The project is packaged using `setuptools`, allowing users to install and run it as a standalone tool from their local environment.
- **Cost-Effectiveness:** Local hosting eliminates server and infrastructure costs while providing immediate execution.

## Infrastructure Components

While a complex infrastructure is unnecessary for this desktop application, the following components ensure smooth operation:

- **File System Utilization:** The file system serves as the backbone for data storage, taking the place of a full-fledged database.
- **Local Environment Tools:**
  - **Standard Libraries:** Modules like `os`, `re`, `shutil`, and `pathlib` facilitate file operations and accurate path management.
  - **Graphical User Interface:** Tkinter is used to provide a user-friendly frontend in addition to the CLI option.
- **Modular Packaging:** The project’s structure enables clear separation of functionality, which aids in debugging and future improvements.

## Security Measures

Even though the primary focus is file export and local execution, some security measures and best practices have been incorporated:

- **Filename Sanitization:** File names are sanitized to avoid issues with different operating systems and to prevent errors during file copying.
- **Error Handling:** Comprehensive error handling routines provide informative messages and prevent the tool from crashing unexpectedly.
- **Minimal Data Exposure:** No external data transmission takes place; all operations remain local, reducing exposure to external threats.

## Monitoring and Maintenance

Given the scope of this project, monitoring and maintenance are kept straightforward:

- **Testing:** Automated tests using `pytest` and coverage analysis with `pytest-cov` ensure that changes do not break the tool's functionality.
- **Logging and Console Messages:** Informative console messages provide feedback during execution and help diagnose issues in real time.
- **Manual Updates:** As the tool is used locally, updates are distributed through package versions, and users can manually upgrade to the latest version.

## Conclusion and Overall Backend Summary

- The backend of the Obsidian Recursive Notes Exporter is a modular, Python-based system that is designed for local execution rather than cloud hosting.
- By leveraging Python 3.6+ along with a set of robust standard libraries and Tkinter for a GUI, the project achieves scalability, maintainability, and effective performance for processing and exporting files.
- Although it does not employ a traditional database, its file system-based approach for storing and organizing data is both efficient and sufficient for its intended purpose.
- Built with careful attention to error handling, filename sanitization, and internal function modularity, the tool remains reliable and easy to maintain.

This backend setup is uniquely tailored to meet the needs of users seeking a straightforward, efficient method of exporting Obsidian notes along with their linked resources, all while ensuring clarity and ease of maintenance for future improvements.