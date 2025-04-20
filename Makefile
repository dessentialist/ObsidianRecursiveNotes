# Makefile for Obsidian Recursive Notes Exporter

.PHONY: test lint clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting (requires flake8)"
	@echo "  make clean      - Clean temporary files"
	@echo "  make help       - Show this help message"

# Run tests
test:
	python -m pytest test_file_counting.py test_gui_interface.py -v

# Run linting
lint:
	@echo "Checking for flake8..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 *.py; \
	else \
		echo "flake8 not installed. Install with: pip install flake8"; \
		exit 1; \
	fi

# Clean temporary files and test artifacts
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc
	rm -rf */__pycache__
	rm -rf */*.pyc
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete 