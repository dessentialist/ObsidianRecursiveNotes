@echo off
echo Starting Obsidian Recursive Notes Exporter...
python run.py
if errorlevel 1 (
    echo Error starting the application.
    echo Please make sure Python 3.6+ is installed and in your PATH.
    pause
) 