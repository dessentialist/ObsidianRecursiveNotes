#!/usr/bin/env python3
"""
Test File Counting Logic

This script tests the file counting logic in the Obsidian Recursive Notes exporter
by creating test files with various link structures and validating the count.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Import the modules to test
from obsidian_recursive_notes.gui_interface import count_expected_links
from obsidian_recursive_notes.file_operations import read_files_recursive


class TestFileCounting(unittest.TestCase):
    """Test cases for file counting logic"""

    def setUp(self):
        """Set up test environment with test files"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.files_copied = []
        
        # Create test directory structure
        os.makedirs(os.path.join(self.test_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "subfolder"), exist_ok=True)
        
        # Create test files
        self.create_test_files()
        
    def tearDown(self):
        """Clean up temporary test files"""
        shutil.rmtree(self.test_dir)
        
    def create_test_files(self):
        """Create test files with various link structures"""
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
        self.main_file = os.path.join(self.test_dir, "main.md")
        with open(self.main_file, "w") as f:
            f.write(main_content)
            
        with open(os.path.join(self.test_dir, "note1.md"), "w") as f:
            f.write(note1_content)
            
        with open(os.path.join(self.test_dir, "note2.md"), "w") as f:
            f.write(note2_content)
            
        with open(os.path.join(self.test_dir, "note3.md"), "w") as f:
            f.write(note3_content)
            
        with open(os.path.join(self.test_dir, "note4.md"), "w") as f:
            f.write(note4_content)
            
        with open(os.path.join(self.test_dir, "note5.md"), "w") as f:
            f.write(note5_content)
            
        with open(os.path.join(self.test_dir, "subfolder", "subnote1.md"), "w") as f:
            f.write(subnote1_content)
            
        # Create image files
        with open(os.path.join(self.test_dir, "test_image.png"), "wb") as f:
            f.write(b"PNG TEST")
            
        with open(os.path.join(self.test_dir, "images", "test_image2.jpg"), "wb") as f:
            f.write(b"JPG TEST")
    
    def test_expected_links_no_depth_limit(self):
        """Test counting expected links with no depth limit"""
        expected_count, visited = count_expected_links(self.main_file)
        
        # We expect 9 files: 
        # - main.md
        # - note1.md through note5.md (5 files)
        # - subfolder/subnote1.md
        # - test_image.png
        # - images/test_image2.jpg
        self.assertEqual(expected_count, 9, f"Expected 9 files, got {expected_count}")
        
        # Check that all expected files are in the visited set
        expected_files = [
            "main.md", "note1.md", "note2.md", "note3.md", "note4.md", "note5.md", 
            "subfolder/subnote1.md", "test_image.png", "images/test_image2.jpg"
        ]
        for file in expected_files:
            file_path = os.path.join(self.test_dir, file.replace("/", os.sep))
            self.assertIn(file_path, visited, f"File {file} should be in visited set")
    
    def test_expected_links_depth_0(self):
        """Test counting expected links with depth limit 0"""
        expected_count, visited = count_expected_links(self.main_file, max_depth=0)
        
        # At depth 0, we expect only the main file
        self.assertEqual(expected_count, 1, f"Expected 1 file, got {expected_count}")
        self.assertEqual(len(visited), 1, f"Expected 1 file in visited set, got {len(visited)}")
    
    def test_expected_links_depth_1(self):
        """Test counting expected links with depth limit 1"""
        expected_count, visited = count_expected_links(self.main_file, max_depth=1)
        
        # At depth 1, we expect main file + directly linked files/images
        # main.md + note1-4.md + subfolder/subnote1.md + 2 images = 8 files
        self.assertEqual(expected_count, 8, f"Expected 8 files, got {expected_count}")
    
    def test_read_files_recursive_consistency(self):
        """Test consistency between expected count and actual copied files"""
        # First get the expected count
        expected_count, visited_files = count_expected_links(self.main_file)
        
        # Print the visited files for debugging
        print("\nExpected files to be copied:")
        for file_path in visited_files:
            print(f"  - {os.path.basename(file_path)}")
        
        # Set up export directory
        export_dir = os.path.join(self.test_dir, "export")
        os.makedirs(export_dir, exist_ok=True)
        os.makedirs(os.path.join(export_dir, "notes"), exist_ok=True)
        
        # Copy the main file
        shutil.copyfile(self.main_file, os.path.join(export_dir, "notes", os.path.basename(self.main_file)))
        files_copied = [self.main_file]
        
        # Process files
        read_files_recursive(
            self.main_file,
            export_dir=export_dir,
            files_already_copied=files_copied
        )
        
        # Print the actually copied files for debugging
        print("\nActually copied files:")
        for file_path in files_copied:
            print(f"  - {os.path.basename(file_path)}")
        
        # Check if the counts match
        self.assertEqual(len(files_copied), expected_count, 
                        f"Expected {expected_count} files, but copied {len(files_copied)}")
        
        # Check that each visited file is in the files_copied list
        for file_path in visited_files:
            self.assertIn(file_path, files_copied, f"File {file_path} should be in files_copied")
    
    def test_circular_reference_handling(self):
        """Test handling of circular references (main -> note1 -> main)"""
        expected_count, visited = count_expected_links(self.main_file)
        
        # Even with circular references, each file should only be counted once
        unique_files = set(visited)
        self.assertEqual(len(unique_files), len(visited), 
                        "Each file should only appear once in the visited set")
    
    def test_non_existent_file_handling(self):
        """Test handling of links to non-existent files"""
        # Start from note5 which has a link to a non-existent file
        note5_path = os.path.join(self.test_dir, "note5.md")
        
        # Count expected links
        expected_count, visited = count_expected_links(note5_path)
        
        # Only note5 itself should be counted
        self.assertEqual(expected_count, 1, 
                        f"Expected 1 file, got {expected_count} (non-existent file should not be counted)")
    
    def test_empty_file_handling(self):
        """Test handling of empty files"""
        # Create an empty file
        empty_file_path = os.path.join(self.test_dir, "empty.md")
        with open(empty_file_path, "w") as f:
            pass
        
        # Count expected links
        expected_count, visited = count_expected_links(empty_file_path)
        
        # Only the empty file itself should be counted
        self.assertEqual(expected_count, 1, 
                        f"Expected 1 file, got {expected_count} (empty file should be counted as 1)")
    
    def test_unicode_handling(self):
        """Test handling of files with Unicode characters"""
        # Create a new temp directory for this test to avoid conflicts
        unicode_test_dir = tempfile.mkdtemp()
        try:
            # Create a file with Unicode characters
            unicode_file_path = os.path.join(unicode_test_dir, "unicode-файл.md")
            unicode_content = """# Unicode Test
            
This file has a link to [[note1]] and Unicode characters.
"""
            with open(unicode_file_path, "w", encoding="utf-8") as f:
                f.write(unicode_content)
            
            # Create the note1 file
            note1_path = os.path.join(unicode_test_dir, "note1.md")
            with open(note1_path, "w", encoding="utf-8") as f:
                f.write("# Note 1\n\nTest file for Unicode test.")
            
            # Count expected links
            expected_count, visited = count_expected_links(unicode_file_path)
            
            # The Unicode file and note1 should be counted
            self.assertEqual(expected_count, 2, 
                            f"Expected 2 files, got {expected_count} (Unicode file handling issue)")
        finally:
            # Clean up
            shutil.rmtree(unicode_test_dir)


if __name__ == "__main__":
    unittest.main() 