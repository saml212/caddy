"""Main entry point for the CAD Agents application."""

import logging
import os
import asyncio
from dotenv import load_dotenv

from .agents.root_agent import root_agent
from .utils.mcp_utils import get_mcp_tools_async, check_mcp_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

async def setup_environment_async():
    """Load environment variables and check connections asynchronously."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required environment variables are set
    if os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "True":
        if not os.getenv("GOOGLE_CLOUD_PROJECT") or not os.getenv("GOOGLE_CLOUD_LOCATION"):
            logger.error("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set when using Vertex AI")
            return False
    else:
        if not os.getenv("GOOGLE_API_KEY"):
            logger.error("GOOGLE_API_KEY must be set when not using Vertex AI")
            return False
    
    # Check MCP connection using the new async method
    logger.info("Checking FreeCAD MCP connection using ADK MCPToolset...")
    try:
        tools, exit_stack = await get_mcp_tools_async()
        
        if tools and exit_stack:
            logger.info(f"Successfully connected to FreeCAD MCP server. Found {len(tools)} tools.")
            
            # Make sure we clean up properly
            await exit_stack.aclose()
            return True
        else:
            logger.warning("Could not connect to FreeCAD MCP server. Make sure it's running.")
            return False
    except Exception as e:
        logger.error(f"Error testing MCP connection: {e}")
        return False

def setup_environment():
    """Load environment variables and check connections synchronously."""
    # For backward compatibility with non-async code
    try:
        return asyncio.run(setup_environment_async())
    except Exception as e:
        logger.error(f"Error in setup_environment: {e}")
        return False

async def start_app_async():
    """Start the CAD Agents application asynchronously."""
    if not await setup_environment_async():
        logger.error("Failed to set up environment. Please check the logs for details.")
        return False
    
    logger.info("Starting CAD Agents application with root agent: %s", root_agent.name)
    
    # In a real application, you would start a web server or other interface here
    # For now, we just return the root agent for the ADK CLI to use
    return root_agent

def start_app():
    """Start the CAD Agents application."""
    # For backward compatibility with non-async code
    try:
        return asyncio.run(start_app_async())
    except Exception as e:
        logger.error(f"Error in start_app: {e}")
        return False

if __name__ == "__main__":
    start_app() 