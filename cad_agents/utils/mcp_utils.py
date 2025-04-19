"""Utilities for interacting with FreeCAD Mission Control Protocol (MCP)."""

import sys
import os
import json
import asyncio
from pathlib import Path
import logging

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

logger = logging.getLogger(__name__)

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
        logger.error(f"Error: FreeCAD MCP directory not found at {mcp_dir}")
        return False

async def get_mcp_tools_async():
    """Get MCP tools from the FreeCAD MCP server using ADK's MCPToolset.
    
    Returns:
        tuple: (tools, exit_stack) - The MCP tools and the exit_stack to close the connection
    """
    # Ensure the MCP environment is set up
    if not setup_mcp_environment():
        logger.error("Failed to set up MCP environment")
        return None, None
    
    try:
        # Get the absolute path to the freecad-mcp module
        root_dir = Path(__file__).parent.parent.parent
        mcp_module_path = root_dir / "freecad-mcp/src"
        
        if not mcp_module_path.exists():
            logger.error(f"FreeCAD MCP module path not found at {mcp_module_path}")
            return None, None
        
        logger.info(f"Attempting to connect to FreeCAD MCP server using module in {mcp_module_path}")
        
        # Use ADK's MCPToolset to connect to the FreeCAD MCP server
        # We're using the module path with -m to run the server correctly
        tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command="python3",  # Use Python 3 to run the server module
                args=[
                    "-m", "freecad_mcp.server"  # Run as a module using the correct import path
                ],
                # Set PYTHONPATH to include the src directory
                env={
                    "PYTHONPATH": f"{str(mcp_module_path)}:{os.getenv('PYTHONPATH', '')}"
                }
            )
        )
        
        logger.info(f"Successfully connected to FreeCAD MCP server, got {len(tools)} tools")
        return tools, exit_stack
    
    except Exception as e:
        logger.error(f"Error connecting to FreeCAD MCP server: {e}")
        return None, None

def get_mcp_client():
    """Get a client instance for the FreeCAD MCP (legacy method).
    
    This is kept for backward compatibility. For new code, use get_mcp_tools_async.
    
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
        logger.error(f"Error importing FreeCAD MCP client: {e}")
        return None
    except Exception as e:
        logger.error(f"Error creating FreeCAD MCP client: {e}")
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
        logger.error(f"Error connecting to FreeCAD MCP server: {e}")
        return False 