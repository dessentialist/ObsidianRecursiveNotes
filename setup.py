#!/usr/bin/env python3
"""
Setup script for Obsidian Recursive Notes Exporter

This allows the package to be installed with pip.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="obsidian-recursive-notes",
    version="1.0.0",
    author="Darpan",
    author_email="your.email@example.com",
    description="A tool to export Obsidian notes and their linked files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/darpan/ObsidianRecursiveNotes",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "obsidian-export=obsidian_recursive_notes.main:main",
            "obsidian-export-gui=obsidian_recursive_notes.gui_interface:main",
        ],
    },
) 