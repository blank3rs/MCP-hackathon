"""
Purpose of the File:
This MCP server provides tools for signaling the start and end of coding sessions
by modifying a status file.

Key Functionality:
- start_coding: Sets the status to True
- done_coding: Sets the status to False

Important Notes & Context:
- Requires 'mcp' library to be installed
- This server can be started with: uv run mcp_mouse_keyboard_server.py
"""

from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp_server = FastMCP(server_name="coding_status_server")

STATUS_FILE = "/Users/akshaym/Documents/hackathons/tests/dl/servers/keep_going.txt"

@mcp_server.tool()
def start_coding() -> str:
    """
    Signals the start of a coding session by setting the status to True.
    
    Returns:
        A string confirming the status was updated
    """
    try:
        with open(STATUS_FILE, 'w') as file:
            file.write("True")
        return "Coding status set to True"
    except Exception as e:
        return f"Error updating status: {str(e)}"

@mcp_server.tool()
def done_coding() -> str:
    """
    Signals the end of a coding session by setting the status to False.
    
    Returns:
        A string confirming the status was updated
    """
    try:
        with open(STATUS_FILE, 'w') as file:
            file.write("False")
        return "Coding status set to False"
    except Exception as e:
        return f"Error updating status: {str(e)}"

if __name__ == "__main__":
    print("Starting Coding Status MCP Server...")
    mcp_server.run(transport='stdio') 