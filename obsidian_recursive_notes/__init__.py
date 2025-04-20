"""
Obsidian Recursive Notes Exporter

A powerful tool to export Obsidian notes and their linked files,
preserving the network of connections while optionally converting to HTML.
"""

__version__ = '1.0.0'
__author__ = 'Darpan'

# Import main components for easier access
from . import file_operations
from . import html_converter
from . import path_utils
from . import gui_interface 