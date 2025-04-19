"""Main entry point for the CAD Agents application."""

import logging
import os
from dotenv import load_dotenv

from .agents.root_agent import root_agent
from .utils.mcp_utils import check_mcp_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Load environment variables and check connections."""
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
    
    # Check MCP connection
    logger.info("Checking FreeCAD MCP connection...")
    if not check_mcp_connection():
        logger.warning("Could not connect to FreeCAD MCP server. Make sure it's running.")
        return False
    
    logger.info("Environment setup completed successfully.")
    return True

def start_app():
    """Start the CAD Agents application."""
    if not setup_environment():
        logger.error("Failed to set up environment. Please check the logs for details.")
        return False
    
    logger.info("Starting CAD Agents application with root agent: %s", root_agent.name)
    
    # In a real application, you would start a web server or other interface here
    # For now, we just return the root agent for the ADK CLI to use
    return root_agent

if __name__ == "__main__":
    start_app() 