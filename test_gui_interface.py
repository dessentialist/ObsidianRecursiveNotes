import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Import the module to be tested
try:
    from obsidian_recursive_notes.gui_interface import select_file, run_export, get_max_depth
except ImportError:
    # Import fallback for running tests directly
    try:
        from obsidian_recursive_notes.gui_interface import select_file, run_export, get_max_depth
    except ImportError:
        pass  # Will be mocked in tests


class TestGUIInterface(unittest.TestCase):
    """Tests for the GUI interface for the Markdown exporter."""

    @patch('obsidian_recursive_notes.gui_interface.create_hidden_root')
    @patch('tkinter.filedialog.askopenfilename')
    def test_select_file(self, mock_askopenfilename, mock_create_root):
        """Test that the file selection dialog returns the selected file path."""
        # Set up the mock to return a specific file path
        mock_root = MagicMock()
        mock_create_root.return_value = mock_root
        expected_path = "/path/to/test.md"
        mock_askopenfilename.return_value = expected_path

        # Call the function
        actual_path = select_file()

        # Check that the function was called with the correct arguments
        mock_askopenfilename.assert_called_once()
        self.assertEqual(actual_path, expected_path)

        # Test when user cancels selection
        mock_askopenfilename.return_value = ""
        actual_path = select_file()
        self.assertIsNone(actual_path)

    @patch('obsidian_recursive_notes.gui_interface.create_hidden_root')
    @patch('tkinter.simpledialog.askinteger')
    def test_get_max_depth(self, mock_askinteger, mock_create_root):
        """Test that the max depth dialog returns the correct value."""
        # Set up mock
        mock_root = MagicMock()
        mock_create_root.return_value = mock_root
        mock_askinteger.return_value = 2

        # Call the function
        max_depth = get_max_depth()

        # Check the result
        self.assertEqual(max_depth, 2)

        # Test with user cancellation
        mock_askinteger.return_value = None
        max_depth = get_max_depth()
        self.assertIsNone(max_depth)

    @patch('obsidian_recursive_notes.gui_interface.read_files_recursive')
    @patch('obsidian_recursive_notes.gui_interface.create_export_dir')
    @patch('obsidian_recursive_notes.gui_interface.resolve_path')
    @patch('obsidian_recursive_notes.gui_interface.ensure_str_path')
    @patch('obsidian_recursive_notes.gui_interface.os.path.exists')
    @patch('obsidian_recursive_notes.gui_interface.os.path.isdir')
    @patch('obsidian_recursive_notes.gui_interface.shutil.rmtree')
    @patch('obsidian_recursive_notes.gui_interface.os.makedirs')
    @patch('obsidian_recursive_notes.gui_interface.shutil.copyfile')
    @patch('obsidian_recursive_notes.gui_interface.count_expected_links')
    @patch('obsidian_recursive_notes.gui_interface.create_hidden_root')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_run_export(self, mock_showerror, mock_showinfo, mock_create_root, mock_count_links, 
                       mock_copyfile, mock_makedirs, mock_rmtree, mock_isdir, 
                       mock_exists, mock_ensure_str_path, mock_resolve_path, 
                       mock_create_export_dir, mock_read_files_recursive):
        """Test that the run_export function calls the correct functions with the right arguments."""
        # Set up mocks
        mock_root = MagicMock()
        mock_create_root.return_value = mock_root
        file_path = "/path/to/test.md"
        resolved_path = "/resolved/path/to/test.md"
        export_dir = "/export/dir"
        
        mock_resolve_path.return_value = (resolved_path, None)
        mock_create_export_dir.return_value = export_dir
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_ensure_str_path.return_value = resolved_path
        mock_count_links.return_value = (5, set())
        
        # Call the function
        result = run_export(file_path, max_depth=2)
        
        # Check the results
        self.assertTrue(result)
        mock_resolve_path.assert_called_once_with(file_path)
        mock_create_export_dir.assert_called_once_with(file_path)
        mock_read_files_recursive.assert_called_once()
        
        # Test when resolve_path returns an error
        mock_resolve_path.return_value = (None, "Error: File not found")
        result = run_export(file_path, max_depth=2)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main() 