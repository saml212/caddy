"""Utilities for interacting with FreeCAD MCP server using MCPToolset."""

import logging
import contextlib
from typing import Optional, Tuple, List, Any

# Need to ensure SseServerParams is imported correctly
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams 

logger = logging.getLogger(__name__)

# Define the MCP server address (assuming SSE on port 5050)
MCP_SERVER_URL = "http://localhost:5050/"

async def load_mcp_tools() -> Tuple[Optional[List[Any]], Optional[contextlib.AsyncExitStack]]:
    """Connect to the FreeCAD MCP server and retrieve its tools using MCPToolset."""
    
    logger.info(f"Attempting to connect to FreeCAD MCP server via SSE at {MCP_SERVER_URL}...")
    
    try:
        # Parameters to connect to the existing MCP server via SSE
        sse_params = SseServerParams(url=MCP_SERVER_URL)
        
        # Use ADK's MCPToolset to connect
        tools, exit_stack = await MCPToolset.from_server(
            connection_params=sse_params
        )
        
        logger.info(f"Successfully connected to FreeCAD MCP server, got {len(tools)} tools")
        return tools, exit_stack
        
    except ImportError:
        # Reraise import error if SseServerParams wasn't found
        logger.error("ImportError: Could not import SseServerParams. Check google-adk installation.")
        raise
    except Exception as e:
        logger.error(f"Error connecting to FreeCAD MCP server at {MCP_SERVER_URL}: {e}", exc_info=True)
        return None, None

async def close_mcp_connection(exit_stack: Optional[contextlib.AsyncExitStack]):
    """Close the MCP connection using the provided exit stack."""
    if exit_stack:
        logger.info("Closing MCP connection...")
        try:
            await exit_stack.aclose()
            logger.info("MCP connection closed.")
        except Exception as e:
            logger.error(f"Error closing MCP connection: {e}", exc_info=True)
    else:
        logger.warning("Attempted to close MCP connection, but no exit stack was provided.")

# Remove previous XML-RPC client logic

# --- Remove or keep legacy functions as needed, currently commented out ---

# def setup_mcp_environment(): ... # Likely not needed for XML-RPC
# async def _initialize_mcp_toolset(): ... # Removed
# async def get_mcp_tool_proxy(tool_name: str): ... # Removed
# def get_mcp_client(): ... # Removed
# def check_mcp_connection(): ... # Removed 