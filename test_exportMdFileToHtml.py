import unittest
import os
import shutil
import tempfile
from pathlib import Path

# Import from refactored modules
from path_utils import ensure_str_path, sanitize_filename, find_rel_path
from file_operations import copy_file_to_export, find_markdown_links, read_files_recursive

class TestExportMdFileToHtml(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.notes_dir = os.path.join(self.test_dir, "notes")
        os.makedirs(self.notes_dir)
        
        # Create test markdown files
        self.main_file = os.path.join(self.notes_dir, "main.md")
        with open(self.main_file, "w") as f:
            f.write("[[linked1.md]]\n[[linked2.md]]\n")
        
        self.linked1_file = os.path.join(self.notes_dir, "linked1.md")
        with open(self.linked1_file, "w") as f:
            f.write("[[linked2.md]]\n")
        
        self.linked2_file = os.path.join(self.notes_dir, "linked2.md")
        with open(self.linked2_file, "w") as f:
            f.write("No links here\n")
    
    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_ensure_str_path(self):
        """Test path conversion function"""
        path = Path("/test/path")
        self.assertEqual(ensure_str_path(path), "/test/path")
        self.assertEqual(ensure_str_path("/test/path"), "/test/path")
        self.assertIsNone(ensure_str_path(None))
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        self.assertEqual(sanitize_filename("test file.md"), "test_file.md")
        self.assertEqual(sanitize_filename("test@file.md"), "test_file.md")
        self.assertEqual(sanitize_filename("test@file#123.md"), "test_file_123.md")
    
    def test_findRelPath(self):
        """Test relative path calculation"""
        self.assertEqual(
            find_rel_path("/test/path/file.md", "/test/current.md"),
            "notes/file.md"
        )
        self.assertEqual(
            find_rel_path("notes/test file.md", "notes/main.md"),
            "notes/test_file.md"
        )
    
    def test_copyFileToExport(self):
        """Test file copying functionality"""
        export_dir = os.path.join(self.test_dir, "export")
        os.makedirs(export_dir)
        
        # Test copying existing file
        result = copy_file_to_export(
            "linked1.md",
            self.main_file,
            export_dir=export_dir
        )
        self.assertEqual(result, "linked1.md")
        self.assertTrue(os.path.exists(os.path.join(export_dir, "notes", "linked1.md")))
        
        # Test copying non-existent file
        result = copy_file_to_export(
            "nonexistent.md",
            self.main_file,
            export_dir=export_dir
        )
        self.assertIsNone(result)
    
    def test_findMdFile(self):
        """Test markdown file link detection"""
        line = "This is a [[test.md]] link"
        result = find_markdown_links(line, self.main_file)
        self.assertIn("test.md", result)
    
    def test_recursion_depth(self):
        """Test recursion depth limiting"""
        export_dir = os.path.join(self.test_dir, "export")
        os.makedirs(export_dir)
        
        # Test with depth 1
        read_files_recursive(
            self.main_file, 
            max_depth=1, 
            export_to_html=False, 
            export_dir=export_dir
        )
        self.assertTrue(os.path.exists(os.path.join(export_dir, "notes", "main.md")))
        self.assertTrue(os.path.exists(os.path.join(export_dir, "notes", "linked1.md")))
        self.assertTrue(os.path.exists(os.path.join(export_dir, "notes", "linked2.md")))
        
        # Clear export directory
        shutil.rmtree(export_dir)
        os.makedirs(export_dir)
        
        # Test with depth 0 - should only copy the main file
        read_files_recursive(
            self.main_file, 
            max_depth=0, 
            export_to_html=False, 
            export_dir=export_dir
        )
        self.assertTrue(os.path.exists(os.path.join(export_dir, "notes", "main.md")))
        self.assertFalse(os.path.exists(os.path.join(export_dir, "notes", "linked1.md")))
        self.assertFalse(os.path.exists(os.path.join(export_dir, "notes", "linked2.md")))
    
    def test_circular_references(self):
        """Test handling of circular references"""
        # Create circular reference
        with open(self.linked2_file, "w") as f:
            f.write("[[main.md]]\n")
        
        export_dir = os.path.join(self.test_dir, "export")
        os.makedirs(export_dir)
        
        # Should not cause infinite recursion
        read_files_recursive(
            self.main_file, 
            export_to_html=False, 
            export_dir=export_dir
        )
        self.assertTrue(os.path.exists(os.path.join(export_dir, "notes", "main.md")))
        self.assertTrue(os.path.exists(os.path.join(export_dir, "notes", "linked1.md")))
        self.assertTrue(os.path.exists(os.path.join(export_dir, "notes", "linked2.md")))
    
    def test_special_characters(self):
        """Test handling of special characters in filenames"""
        special_file = os.path.join(self.notes_dir, "test@file.md")
        with open(special_file, "w") as f:
            f.write("Test content\n")
        
        export_dir = os.path.join(self.test_dir, "export")
        os.makedirs(export_dir)
        
        result = copy_file_to_export(
            "test@file.md",
            self.main_file,
            export_dir=export_dir
        )
        self.assertEqual(result, "test@file.md")
        self.assertTrue(os.path.exists(os.path.join(export_dir, "notes", "test@file.md")))

if __name__ == "__main__":
    unittest.main() 