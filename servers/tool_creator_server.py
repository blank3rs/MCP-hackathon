"""
File: servers/tool_creator_server.py
Purpose: This file defines the primary Model Context Protocol (MCP) server (Server 1).
         Its main tool, 'create_tool', now acts as a placeholder that logs its input parameters.
Key Functionality:
- Initializes a FastMCP server ('tool_creator_server').
- Defines an asynchronous tool 'create_tool'.
- 'create_tool' prints the tool_name and tool_description it receives.
- Defines a tool 'list_files' that lists all Python files in a directory.
- Runs the MCP server using streamable-http transport on host 0.0.0.0, port 8002.
Important Notes & Context:
- The 'create_tool' function's primary role is a placeholder.
- Communication with a secondary server has been removed.
- This server (tool_creator_server) runs on port 8002.
"""
import asyncio
from mcp.server.fastmcp import FastMCP
from typing import Any, Dict, List
from datetime import timedelta
import time
from mcp import ClientSession, types as mcp_types
from mcp.client.streamable_http import streamablehttp_client
from contextlib import AsyncExitStack

# Import coder_setup functions
from tools.default.coder_setup import start_inspector_and_refresh, paste_formatted_string

# Import the new list_files tool
from tools.file_ops.list_files import list_files

# Global variables to manage the client connection to the secondary server
secondary_client_session: ClientSession | None = None
secondary_server_connection_stack: AsyncExitStack | None = None
# --- End Configuration ---


# Initialize FastMCP server
host_param_tcs = "0.0.0.0" # For Tool Creator Server
port_param_tcs = 8000   # For Tool Creator Server
mcp = FastMCP(
    server_name="tool_creator_server",
    host=host_param_tcs,
    port=port_param_tcs
)

@mcp.tool()
async def create_tool(tool_name: str, tool_description: str) -> Dict[str, Any]:
    """
    Creates a tool by using the coder_setup functions to automate the process.
    This tool now calls the GUI automation functions in coder_setup.py.

    Args:
        tool_name: The name of the tool to be created.
        tool_description: A description of the tool to be created.

    Returns:
        A dictionary indicating the status and parameters received.
    """
    print(f"[ToolCreatorServer] Received call to create_tool.")
    print(f"[ToolCreatorServer] Tool Name: {tool_name}")
    print(f"[ToolCreatorServer] Tool Description: {tool_description}")
    
    try:
        # Start the inspector and refresh it
        start_inspector_and_refresh()
        
        # Create a formatted prompt with the tool description
        tool_prompt = f"build a tool named {tool_name} that {tool_description}"
        paste_formatted_string(tool_prompt)
        
        return {
            "status": "success",
            "message": f"Successfully initiated creation of tool '{tool_name}' with description '{tool_description}'.",
            "received_tool_name": tool_name,
            "received_tool_description": tool_description
        }
    except Exception as e:
        error_message = f"Error creating tool: {str(e)}"
        print(f"[ToolCreatorServer] {error_message}")
        return {
            "status": "error",
            "message": error_message,
            "received_tool_name": tool_name,
            "received_tool_description": tool_description
        }

@mcp.tool()
def list_python_files() -> Dict[str, Any]:
    """
    Lists all Python files in the current directory.
    
    Returns:
        A dictionary containing the list of Python files found in the current directory.
    """
    return list_files()


if __name__ == "__main__":
    loop = asyncio.get_event_loop() # Re-adding for the original cleanup logic
    host = "0.0.0.0" # This remains for the print statements
    port = 8000    # This remains for the print statements
    try:
        mcp.run(
            transport='streamable-http'
        )
        print(f"MCP Server 'tool_creator_server' started on streamable-http, host {host}, port {port}")
    except KeyboardInterrupt:
        print("[ToolCreatorServer] Server shutting down...")
    finally:
        print("[ToolCreatorServer] Attempting to clean up resources...")
        # No specific cleanup needed anymore for secondary client
    print("[ToolCreatorServer] MCP Server shutdown complete.") 