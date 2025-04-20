import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Import the module to be tested
# (We'll create this after writing the tests)
try:
    from gui_interface import select_file, get_export_options, run_export
except ImportError:
    pass  # Will be created after the tests


class TestGUIInterface(unittest.TestCase):
    """Tests for the GUI interface for the Markdown exporter."""

    @patch('gui_interface.filedialog.askopenfilename')
    def test_select_file(self, mock_askopenfilename):
        """Test that the file selection dialog returns the selected file path."""
        # Set up the mock to return a specific file path
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

    @patch('gui_interface.simpledialog.askinteger')
    @patch('gui_interface.messagebox.askyesno')
    def test_get_export_options(self, mock_askyesno, mock_askinteger):
        """Test that the export options dialog returns the correct values."""
        # Set up mocks
        mock_askyesno.return_value = True
        mock_askinteger.return_value = 2

        # Call the function
        export_to_html, max_depth = get_export_options()

        # Check the results
        self.assertTrue(export_to_html)
        self.assertEqual(max_depth, 2)

        # Test with different values
        mock_askyesno.return_value = False
        mock_askinteger.return_value = None  # User cancelled
        
        export_to_html, max_depth = get_export_options()
        
        self.assertFalse(export_to_html)
        self.assertIsNone(max_depth)

    @patch('gui_interface.read_files_recursive')
    @patch('gui_interface.create_export_dir')
    @patch('gui_interface.resolve_path')
    @patch('gui_interface.ensure_str_path')
    @patch('gui_interface.generate_treeview_html')
    @patch('gui_interface.os.path.exists')
    @patch('gui_interface.os.path.isdir')
    @patch('gui_interface.shutil.rmtree')
    @patch('gui_interface.os.makedirs')
    @patch('gui_interface.shutil.copyfile')
    @patch('gui_interface.open')
    def test_run_export(self, mock_open, mock_copyfile, mock_makedirs, mock_rmtree, 
                        mock_isdir, mock_exists, mock_generate_treeview, 
                        mock_ensure_str_path, mock_resolve_path, mock_create_export_dir,
                        mock_read_files_recursive):
        """Test that the run_export function calls the correct functions with the right arguments."""
        # Set up mocks
        file_path = "/path/to/test.md"
        resolved_path = "/resolved/path/to/test.md"
        export_dir = "/export/dir"
        
        mock_resolve_path.return_value = (resolved_path, None)
        mock_create_export_dir.return_value = export_dir
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_ensure_str_path.return_value = resolved_path
        
        # Mock the file open
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Call the function
        result = run_export(file_path, export_to_html=True, max_depth=2)
        
        # Check the results
        self.assertTrue(result)
        mock_resolve_path.assert_called_once_with(file_path)
        mock_create_export_dir.assert_called_once_with(file_path)
        mock_read_files_recursive.assert_called_once()
        
        # Test when resolve_path returns an error
        mock_resolve_path.return_value = (None, "Error: File not found")
        result = run_export(file_path, export_to_html=True, max_depth=2)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main() 