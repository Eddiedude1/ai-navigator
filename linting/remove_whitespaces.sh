#!/bin/bash

# Script to remove trailing whitespace from Python files using VIM
# Usage: ./clean_py_whitespace.sh [file1.py] [file2.py] ...
# Or: ./clean_py_whitespace.sh (to process all .py files in current directory)

if [ $# -eq 0 ]; then
    # No arguments provided - process all .py files in current directory
    py_files=(*.py)
    
    # Check if any .py files exist
    if [ ! -e "${py_files[0]}" ]; then
        echo "No .py files found in current directory"
        exit 1
    fi
    
    echo "Processing all .py files in current directory..."
    for file in *.py; do
        if [ -f "$file" ]; then
            echo "Cleaning: $file"
            vim -c ':%s/\s\+$//e' -c ':wq' "$file"
        fi
    done
else
    # Process specified files
    for file in "$@"; do
        if [ ! -f "$file" ]; then
            echo "Warning: File '$file' not found, skipping..."
            continue
        fi
        
        # Check if it's a Python file
        if [[ "$file" != *.py ]]; then
            echo "Warning: '$file' is not a .py file, skipping..."
            continue
        fi
        
        echo "Cleaning: $file"
        vim -c ':%s/\s\+$//e' -c ':wq' "$file"
    done
fi

echo "Done!"
