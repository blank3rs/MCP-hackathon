import argparse
import sys
import os
import json
from functions.findMCP import find_and_display_mcp_servers
from functions.getConfig import get_config_for_url

def get_new_mcp(query, interactive=False):
    """
    Find an MCP server based on query and get its configuration.
    
    Args:
        query (str): Search term to find MCP server
        interactive (bool): Whether to run in interactive mode
        
    Returns:
        tuple: (server_info, config) where server_info is dict with server details
               and config is the configuration for that server
    """
    # Find MCP servers matching the query
    results = find_and_display_mcp_servers(
        query=query,
        limit=1,
        json_output=True,
        interactive=interactive
    )
    
    if not results or len(results) == 0:
        print(f"No MCP servers found matching '{query}'")
        return None, None
    
    # Get the first result
    server = results[0]
    repository_url = server["repository"]
    
    # Get configuration for this repository URL
    config = get_config_for_url(repository_url)
    
    if not config:
        print(f"No configuration found for {repository_url}")
    
    return server, config

def update_mcp_json(server_name, config, json_path=None):
    """
    Update the mcp.json file with a new server configuration.
    
    Args:
        server_name (str): Name of the MCP server to add
        config (dict): Configuration for the server
        json_path (str, optional): Path to the mcp.json file.
                                  Defaults to ~/.cursor/mcp.json
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not json_path:
        home_dir = os.path.expanduser("~")
        json_path = os.path.join(home_dir, ".cursor", "mcp.json")
    
    print(f"Updating MCP configuration at: {json_path}")
    
    try:
        # Read existing config
        with open(json_path, 'r') as f:
            mcp_config = json.load(f)
        
        # Add or update server configuration
        if 'mcpServers' not in mcp_config:
            mcp_config['mcpServers'] = {}
        
        # Print before update for debugging
        print(f"Current servers: {list(mcp_config['mcpServers'].keys())}")
        
        # Add new server to the configuration
        mcp_config['mcpServers'][server_name] = config
        
        # Print after update for debugging
        print(f"Updated servers: {list(mcp_config['mcpServers'].keys())}")
        
        # Write updated config back to file
        with open(json_path, 'w') as f:
            json.dump(mcp_config, f, indent=4)
        
        print(f"Successfully added/updated {server_name} in {json_path}")
        return True
    
    except Exception as e:
        print(f"Error updating mcp.json: {str(e)}")
        return False

def install_missing_mcp_server(server_name, interactive=False):
    """
    Install a missing MCP server configuration by name.
    
    Args:
        server_name (str): Name of the MCP server to install
        interactive (bool): Whether to run in interactive mode
        
    Returns:
        dict: Result information including success status and messages
    """
    # Search for the server by name
    results = find_and_display_mcp_servers(
        query=server_name,
        limit=1,
        json_output=True,
        interactive=False
    )
    
    if not results or len(results) == 0:
        print(f"No MCP servers found matching '{server_name}'")
        return {"success": False, "message": f"No MCP servers found matching '{server_name}'"}
    
    # Get the first result
    server = results[0]
    repository_url = server["repository"]
    
    # Get configuration for this repository URL
    config = get_config_for_url(repository_url)
    
    if not config:
        print(f"No configuration found for {repository_url}")
        return {"success": False, "message": f"No configuration found for {repository_url}"}
    
    # Update mcp.json with the new server
    home_dir = os.path.expanduser("~")
    json_path = os.path.join(home_dir, ".cursor", "mcp.json")
    
    success = update_mcp_json(server["name"], config, json_path)
    
    if success:
        return {
            "success": True, 
            "message": f"Successfully installed {server['name']} MCP server",
            "server": server,
            "config": config
        }
    else:
        return {
            "success": False,
            "message": f"Failed to install {server['name']} MCP server"
        }

def main():
    """
    Main entry point for the script when run from command line.
    Parses arguments and displays results.
    """
    parser = argparse.ArgumentParser(description="Find an MCP server and get its configuration")
    parser.add_argument("query", nargs="?", default="", help="Search term for MCP server")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--update-json", "-u", action="store_true", help="Update mcp.json with the server configuration")
    parser.add_argument("--json-path", help="Path to mcp.json file (default: ~/.cursor/mcp.json)")
    parser.add_argument("--install", action="store_true", help="Install the MCP server configuration")
    parser.add_argument("--no-update", action="store_true", help="Don't update mcp.json automatically")
    
    args = parser.parse_args()
    
    # Handle install mode
    if args.install and args.query:
        result = install_missing_mcp_server(args.query, args.interactive)
        if result["success"]:
            print(result["message"])
        else:
            print(f"Error: {result['message']}")
        return
    
    # Regular mode
    server, config = get_new_mcp(args.query, args.interactive)
    
    if server and config:
        print(f"\nServer Configuration for {server['name']}:")
        print(f"  Command: {config['command']}")
        print(f"  Args: {config['args']}")
        if 'env' in config:
            print(f"  Environment Variables: {config['env']}")
        
        # Always update JSON unless explicitly told not to
        if not args.no_update:
            success = update_mcp_json(server['name'], config, args.json_path)
            if success:
                print(f"\nMCP server '{server['name']}' has been added to mcp.json")
            else:
                print(f"\nFailed to add MCP server '{server['name']}' to mcp.json")

if __name__ == "__main__":
    main()
