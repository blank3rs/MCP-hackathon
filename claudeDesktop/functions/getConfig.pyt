def get_config():
    return {
        "mcpServers": {
            "https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
            },
            "https://github.com/modelcontextprotocol/servers/tree/main/src/git": {
                "command": "uvx",
                "args": ["mcp-server-git"]
            },
            "https://github.com/modelcontextprotocol/servers/tree/main/src/everything": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-everything"]
            },
            "https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "/Users/pragalvhasharma/Downloads/PragGOToDocuments/Blanc/school/mcpServers/McpSkeleton/claudeDesktop"
                ]
            },
            "https://github.com/modelcontextprotocol/servers/tree/main/src/github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": "REMOVED_TOKEN"
                }
            },
            "https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                "env": {
                    "BRAVE_API_KEY": "BSAKlSpKxvNfwsX7zQapClc8k7c1Tvj"
                }
            }
        }
    }

# Test function to retrieve configuration for a given URL
def get_config_for_url(url):
    config = get_config()
    return config["mcpServers"].get(url, None)

# Main test section
if __name__ == "__main__":
    # Sample URL test
    sample_url = "https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer"
    config = get_config_for_url(sample_url)
    
    if config:
        print(f"Configuration for {sample_url}:")
        print(f"  Command: {config['command']}")
        print(f"  Args: {config['args']}")
    else:
        print(f"No configuration found for {sample_url}")
