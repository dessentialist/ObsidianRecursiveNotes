#!/usr/bin/env python3
"""
Manual Test Script for Obsidian Recursive Notes Exporter

This script helps manually test the Obsidian Recursive Notes exporter
with custom test files and directories.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

from gui_interface import count_expected_links, run_export
from file_operations import read_files_recursive


def create_test_vault():
    """Create a test Obsidian vault with sample content"""
    # Create a temporary directory for test files
    test_dir = tempfile.mkdtemp()
    print(f"Creating test vault at: {test_dir}")
    
    # Create test directory structure
    os.makedirs(os.path.join(test_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(test_dir, "subfolder"), exist_ok=True)
    
    # Main file with links to other files and images
    main_content = """# Main Test File
    
This is a test file with links to other markdown files and images.

## Links to Markdown Files
- Regular link: [[note1]]
- Link with extension: [[note2.md]]
- Link with anchor: [[note3#section]]
- Link with alias: [[note4|Alias for Note 4]]
- Link to subfolder: [[subfolder/subnote1]]

## Links to Images
- Standard image: ![[test_image.png]]
- Image in subfolder: ![[images/test_image2.jpg]]

## External Links
- [External Link](https://example.com)
"""
    
    # Note 1 with circular link back to main
    note1_content = """# Note 1
    
This is Note 1 with a link back to [[main]].

It also has a new link to [[note5]].
"""
    
    # Note 2 with no links
    note2_content = """# Note 2
    
This file has no links to other files.
"""
    
    # Note 3 with links and an image
    note3_content = """# Note 3

## Section

This file has a section and links to [[note2]] and an image ![[test_image.png]].
"""
    
    # Note 4 with a self-reference
    note4_content = """# Note 4
    
This file has a self-reference link: [[#section]].

## Section
Content in section.
"""
    
    # Note 5 with link to non-existent file
    note5_content = """# Note 5
    
This file has a link to a [[non-existent-file]] that doesn't exist.
"""
    
    # Subnote 1 in subfolder
    subnote1_content = """# Subnote 1
    
This file is in a subfolder and links to [[../note1]].
"""
    
    # Write files
    main_file = os.path.join(test_dir, "main.md")
    with open(main_file, "w") as f:
        f.write(main_content)
        
    with open(os.path.join(test_dir, "note1.md"), "w") as f:
        f.write(note1_content)
        
    with open(os.path.join(test_dir, "note2.md"), "w") as f:
        f.write(note2_content)
        
    with open(os.path.join(test_dir, "note3.md"), "w") as f:
        f.write(note3_content)
        
    with open(os.path.join(test_dir, "note4.md"), "w") as f:
        f.write(note4_content)
        
    with open(os.path.join(test_dir, "note5.md"), "w") as f:
        f.write(note5_content)
        
    with open(os.path.join(test_dir, "subfolder", "subnote1.md"), "w") as f:
        f.write(subnote1_content)
        
    # Create image files
    with open(os.path.join(test_dir, "test_image.png"), "wb") as f:
        f.write(b"PNG TEST")
        
    with open(os.path.join(test_dir, "images", "test_image2.jpg"), "wb") as f:
        f.write(b"JPG TEST")
    
    return test_dir, main_file


def cleanup_test_vault(test_dir):
    """Clean up the test vault"""
    try:
        shutil.rmtree(test_dir)
        print(f"Cleaned up test vault at: {test_dir}")
    except Exception as e:
        print(f"Warning: Could not clean up test vault: {e}")


def run_test():
    """Run the test"""
    # Create test vault
    test_dir, main_file = create_test_vault()
    
    try:
        # Count expected files
        print("\nCounting expected files...")
        expected_count, visited = count_expected_links(main_file)
        print(f"Expected file count: {expected_count}")
        print("Files that should be included:")
        for path in visited:
            print(f"  - {path}")
        
        # Test with no depth limit
        print("\nTesting with no depth limit...")
        run_export(main_file, export_to_html=True, max_depth=None)
        
        # Test with depth limit 1
        print("\nTesting with depth limit 1...")
        run_export(main_file, export_to_html=True, max_depth=1)
        
        # Test with depth limit 0
        print("\nTesting with depth limit 0...")
        run_export(main_file, export_to_html=True, max_depth=0)
        
        print("\nManual test completed successfully!")
    finally:
        # Cleanup test files
        response = input("Do you want to clean up the test vault? (y/n): ")
        if response.lower() == 'y':
            cleanup_test_vault(test_dir)
        else:
            print(f"Test vault remains at: {test_dir}")


if __name__ == "__main__":
    run_test() 