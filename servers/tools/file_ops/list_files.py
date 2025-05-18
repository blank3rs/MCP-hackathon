"""
File: servers/tools/file_ops/list_files.py
Purpose: Implements a tool that lists all Python files in the current directory.
"""

import os
from typing import List, Dict, Any

def list_files() -> Dict[str, Any]:
    """
    Lists all Python files in the current directory.
    
    Returns:
        A dictionary containing the list of Python files found in the current directory.
    """
    try:
        # Get the current directory
        current_directory = os.getcwd()
        
        # Get all Python files in the current directory
        python_files = [
            file for file in os.listdir(current_directory) 
            if file.endswith(".py")
        ]
        
        # Return the list of Python files
        return {
            "status": "success",
            "message": f"Successfully listed {len(python_files)} Python files in directory: {current_directory}",
            "python_files": python_files,
            "directory": current_directory
        }
    except Exception as e:
        # Return error message if something goes wrong
        error_message = f"Error listing Python files: {str(e)}"
        print(f"[list_files] {error_message}")
        return {
            "status": "error",
            "message": error_message,
            "python_files": [],
            "directory": os.getcwd()
        } 