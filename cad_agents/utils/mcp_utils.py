"""Utilities for interacting with FreeCAD Mission Control Protocol (MCP)."""

import sys
import os
import json
from pathlib import Path

# Add the freecad-mcp submodule to the Python path
def setup_mcp_environment():
    """Set up the environment to use FreeCAD MCP.
    
    Adds the freecad-mcp directory to the Python path.
    """
    # Get the project root directory
    root_dir = Path(__file__).parent.parent.parent
    mcp_dir = root_dir / "freecad-mcp"
    
    if mcp_dir.exists():
        if str(mcp_dir) not in sys.path:
            sys.path.append(str(mcp_dir))
        return True
    else:
        print(f"Error: FreeCAD MCP directory not found at {mcp_dir}")
        return False

def get_mcp_client():
    """Get a client instance for the FreeCAD MCP.
    
    Returns:
        A client instance if successful, None otherwise.
    """
    if not setup_mcp_environment():
        return None
    
    try:
        from freecad_mcp.client import Client
        client = Client()
        return client
    except ImportError as e:
        print(f"Error importing FreeCAD MCP client: {e}")
        return None
    except Exception as e:
        print(f"Error creating FreeCAD MCP client: {e}")
        return None

def check_mcp_connection():
    """Check if we can connect to the FreeCAD MCP server.
    
    Returns:
        bool: True if connection is successful, False otherwise.
    """
    client = get_mcp_client()
    if client is None:
        return False
    
    try:
        # Test the connection with a simple command
        version = client.get_version()
        return True
    except Exception as e:
        print(f"Error connecting to FreeCAD MCP server: {e}")
        return False 