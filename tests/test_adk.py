#!/usr/bin/env python3
"""Test script to verify the CAD Agents ADK setup."""

import asyncio
import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import CAD Agents modules
from cad_agents.utils.mcp_utils import get_mcp_tools_async
from cad_agents.agents.root_agent import root_agent

async def test_adk_setup():
    """Test the ADK setup by checking model capabilities and MCP connection."""
    logger.info("Testing ADK setup with model: %s", root_agent.model)
    
    # Load environment variables
    load_dotenv()
    
    # 1. Check environment variables
    logger.info("Checking environment variables...")
    if os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "True":
        if not os.getenv("GOOGLE_CLOUD_PROJECT") or not os.getenv("GOOGLE_CLOUD_LOCATION"):
            logger.error("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set when using Vertex AI")
            return False
        logger.info("Using Vertex AI with project: %s, location: %s", 
                   os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_LOCATION"))
    else:
        if not os.getenv("GOOGLE_API_KEY"):
            logger.error("GOOGLE_API_KEY must be set when not using Vertex AI")
            return False
        logger.info("Using Google AI Studio with API key")
    
    # 2. Test MCP connection
    logger.info("Testing MCP connection...")
    try:
        tools, exit_stack = await get_mcp_tools_async()
        
        if tools and exit_stack:
            tool_names = [tool.name for tool in tools]
            logger.info(f"Successfully connected to FreeCAD MCP server. Found tools: {tool_names}")
            
            # Make sure we clean up properly
            await exit_stack.aclose()
            logger.info("MCP connection test passed")
        else:
            logger.warning("Could not connect to FreeCAD MCP server. Make sure it's running.")
            return False
    except Exception as e:
        logger.error(f"Error testing MCP connection: {e}")
        return False
    
    logger.info("ADK setup test completed successfully")
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(test_adk_setup())
        if result:
            logger.info("✅ All tests passed! Your ADK setup is working correctly.")
            sys.exit(0)
        else:
            logger.error("❌ Tests failed. Check the logs above for details.")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        sys.exit(1) 