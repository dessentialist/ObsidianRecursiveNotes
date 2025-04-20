# Project Requirements Document (PRD)

This document provides a detailed description of the Obsidian Recursive Notes Exporter project, outlining its core problem, objectives, functionalities, and technical aspects. It serves as the definitive reference for creating further technical documents and guidelines about the project.

## 1. Project Overview

The Obsidian Recursive Notes Exporter is a Python-based tool designed to help users export their Obsidian Markdown notes along with any files linked within them, including other Markdown documents and images. By automatically traversing files and maintaining the internal linking structure, the tool simplifies the process of consolidating related notes and ensures that no important reference is missed—even when links may create circular references.

The tool is being built to address the cumbersome process of manually handling interconnected notes in Obsidian. Its key objectives include providing both a command-line interface (CLI) and a graphical user interface (GUI) to cater to different user preferences, allowing custom control over the recursion depth, and ensuring a clean export directory structure that maintains file relationships. The success criteria for this project are robust error handling, intuitive usability, and preserved data integrity during export with consistent handling of edge cases like circular references and Unicode filenames.

### Goal

The goal of the app is to fetch all related files form a wikilinks styled repository of .md files. Specifically, I've built this to fetch all related files from Obsidian easily, to allow me to use it in RAG repositories.

## 2. In-Scope vs. Out-of-Scope

**In-Scope:**

*   Development of both GUI and CLI interfaces for starting an export operation.
*   Recursive file traversal for Markdown and image links with customizable depth settings.
*   Handling circular references to prevent infinite loops during the export process.
*   Estimation and display of the number of files to be exported before the operation begins (GUI only).
*   Creating a clean, organized export directory with subdirectories for notes and images.
*   Filename sanitization for cross-platform compatibility and Unicode support.
*   Comprehensive error handling with informative messages for missing files or other issues encountered during export.
*   Packaging, distribution, and testing using standard Python tools (e.g., setuptools, pytest).

**Out-of-Scope:**

*   Integration with external storage solutions or cloud services for file export.
*   Real-time collaborative editing or multi-user support.
*   Advanced visual editing or note editing capabilities within the application.
*   Extensive customization of export formats (the focus is on a directory structure with basic organization).
*   Support for file types beyond Markdown and common image formats.
*   Non-Python based implementations or support for Python versions below 3.6.

## 3. User Flow

A typical user journey begins when a user launches the application either through the GUI or the CLI. In the GUI, the user runs the provided script (such as run.py, run.sh, or run_gui.bat), selects a Markdown file using a file dialog, and sets the desired recursion depth to control how many levels of linked files should be exported. Those comfortable with command-line operations can directly run the main script with the file path and optional depth parameter to initiate the export process.

After the file is selected, the application handles argument parsing and path resolution, ensuring the file exists and converting it to an absolute path. The system then creates an export directory (by default on the desktop or another specified base directory) and, if applicable, estimates the number of files to be processed. The application recursively traverses the chosen Markdown file and its links, copies the relevant files (including linked Markdown files and images) into the organized structure, and finally informs the user of the successful export along with any file count statistics and warnings.

## 4. Core Features (Bullet Points)

*   **Recursive Export:**

    *   Traverses Markdown files and automatically identifies all links to other Markdown documents and images.
    *   Recursively processes linked files up to a user-specified maximum depth.

*   **Customizable Recursion Depth:**

    *   Allows users to define how deep the export should scan for linked files, with a depth value of 0 exporting only the initial file and higher values allowing broader recursion.

*   **Circular Reference Handling:**

    *   Detects loops in file references to prevent infinite recursion and ensures a safe termination of the export process.

*   **Dual Interfaces (GUI and CLI):**

    *   GUI: A user-friendly graphical interface using Tkinter that enables file selection and setting parameters via dialogs and input fields.
    *   CLI: A command-line interface that provides flexibility for automation and advanced usage scenarios.

*   **File Counting:**

    *   Pre-export estimation by counting the expected number of files (only in the GUI) to give users insight into what will be exported.

*   **Organized Output Structure:**

    *   Exports files into a structured directory (commonly with an 'export' folder containing a 'notes' subdirectory and separate folder for images).

*   **Unicode and Filename Sanitization:**

    *   Supports filenames and file contents with Unicode characters and sanitizes filenames to ensure cross-platform compatibility.

*   **Robust Error Handling:**

    *   Provides clear, informative error messages in case of missing files, permission issues, or other errors during file processing.

## 5. Tech Stack & Tools

*   **Frontend Frameworks / GUI:**

    *   Tkinter (Python’s standard library for GUI creation) will be used to develop the graphical interface.

*   **Backend Frameworks / Languages:**

    *   Python 3.6+ is the core programming language for the project, leveraging libraries such as os, re, shutil, and pathlib for file operations.

*   **Testing and Packaging:**

    *   setuptools for packaging and distribution.
    *   pytest and pytest-cov for unit testing and code coverage analysis.

*   **Additional Tools:**

    *   Cursor: An advanced IDE assisting with real-time code suggestions, which may integrate into the development process.
    *   Replit: An online IDE used for code collaboration and development, suitable for prototyping the project.

*   **AI Models/Libraries:**

    *   While there is no direct integration with AI models like GPT-4 o, the PRD and subsequent documents are formulated to ensure clarity and maintainability.

## 6. Non-Functional Requirements

*   **Performance:**

    *   The tool should efficiently process files with minimal delays. Users should see a responsive interface and quick file counting results in the GUI.

*   **Security:**

    *   Ensure safe handling of file operations to avoid unauthorized access. Sanitize filenames to prevent security issues related to file system operations.

*   **Usability:**

    *   The application must be user-friendly, with clear prompts and instructions in the GUI, and detailed usage messages in the CLI.

*   **Reliability:**

    *   The exporter should handle edge cases such as missing files or circular references without crashing, ensuring graceful error recovery.

*   **Compliance:**

    *   Adherence to Python’s best practices and packaging guidelines for distributing and installing third-party Python tools.

*   **Response Times:**

    *   Target load times should not exceed a few seconds for typical note directories. File export operations should process incrementally, providing feedback if delays occur.

## 7. Constraints & Assumptions

*   **Python Version Dependency:**

    *   The project assumes availability of Python 3.6 or higher.

*   **File System Permissions:**

    *   It assumes that users have sufficient file system permissions to read source files and create directories for export.

*   **Input Validity:**

    *   It is assumed that the input Markdown file exists and follows basic markdown linking conventions.

*   **Platform Assumptions:**

    *   Although cross-platform compatibility is a goal, slight differences may exist between operating systems regarding file path delimiter handling and permissions.

*   **Tool Availability:**

    *   The project assumes that Tkinter is available in the target Python installations, which is common in the standard library.
    *   It also assumes availability of external packages for testing and packaging such as setuptools and pytest.

## 8. Known Issues & Potential Pitfalls

*   **Circular References:**

    *   Circular links might lead to recursive loops if not handled carefully. The implemented safeguard must correctly detect and break these links to avoid infinite processing.

*   **File Path Handling:**

    *   Differences in file path formats across operating systems (Windows vs. macOS vs. Linux) can introduce issues. A robust file path resolution function is required to mitigate this.

*   **Performance Bottlenecks:**

    *   For large note directories with numerous deep links, recursive processing could become slow. Consider adding optimizations or progress indicators to improve user experience.

*   **Filename Conflicts:**

    *   Sanitizing filenames is critical to prevent conflicts, particularly when files with similar names exist. It might be necessary to implement additional checks to avoid overwriting files.

*   **User Input Errors:**

    *   In the CLI mode, incorrect or missing arguments could lead to errors. Comprehensive input validation and detailed usage instructions are necessary to mitigate these issues.

*   **Dependency on Standard Libraries:**

    *   While the reliance on Python’s standard libraries simplifies development, any unexpected behavior or incompatibility in these libraries (especially across different platforms) could affect the tool’s stability.

This PRD is now our single source of truth for all further documentation and development guidelines regarding the Obsidian Recursive Notes Exporter. Every subsequent technical document should refer back to this document to ensure consistency across the project.
