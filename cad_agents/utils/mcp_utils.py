"""Utilities for interacting with FreeCAD Mission Control Protocol (MCP)."""

import sys
import os
import json
import asyncio
from pathlib import Path
import logging

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

logger = logging.getLogger(__name__)

# Add the freecad-mcp submodule's src directory to the Python path
def setup_mcp_environment():
    """Set up the environment to use FreeCAD MCP.
    
    Adds the freecad-mcp/src directory to the Python path.
    """
    # Get the project root directory
    root_dir = Path(__file__).parent.parent.parent
    mcp_src_dir = root_dir / "freecad-mcp" / "src"
    
    if mcp_src_dir.exists():
        if str(mcp_src_dir) not in sys.path:
            sys.path.insert(0, str(mcp_src_dir)) # Use insert(0, ...) for higher precedence
            logger.debug(f"Added {mcp_src_dir} to Python path")
        return True
    else:
        logger.error(f"Error: FreeCAD MCP source directory not found at {mcp_src_dir}")
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
        # Get the absolute path to the freecad-mcp module src directory
        root_dir = Path(__file__).parent.parent.parent
        mcp_src_dir = root_dir / "freecad-mcp" / "src"
        
        if not mcp_src_dir.exists():
            logger.error(f"FreeCAD MCP src directory not found at {mcp_src_dir}")
            return None, None
        
        logger.info(f"Attempting to connect to FreeCAD MCP server using module in {mcp_src_dir}")
        
        # Use ADK's MCPToolset to connect to the FreeCAD MCP server
        # We're using the module path with -m to run the server correctly
        tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command=sys.executable,  # Use current Python executable
                args=[
                    "-m", "freecad_mcp.server"  # Run as a module using the correct import path
                ],
                # Set PYTHONPATH to include the src directory
                env={
                    "PYTHONPATH": f"{str(mcp_src_dir)}{os.pathsep}{os.getenv('PYTHONPATH', '')}"
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
        # Test the connection with a simple command (using the legacy client)
        # Replace with a lightweight RPC call if possible
        docs = client.list_documents() # Use a simple call like list_documents
        logger.info("Successfully connected to FreeCAD MCP server via legacy client.")
        return True
    except Exception as e:
        logger.error(f"Error connecting to FreeCAD MCP server via legacy client: {e}")
        return False 