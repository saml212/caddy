#!/usr/bin/env python3
"""Simple script to test the MCP connection to FreeCAD."""

import sys
import logging
from pathlib import Path
import importlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Add the freecad-mcp submodule to the Python path
def setup_mcp_environment():
    """Set up the environment to use FreeCAD MCP."""
    # Get the project root directory
    root_dir = Path(__file__).parent
    mcp_src_dir = root_dir / "freecad-mcp" / "src"
    
    if mcp_src_dir.exists():
        if str(mcp_src_dir) not in sys.path:
            sys.path.append(str(mcp_src_dir))
        logger.info(f"Added {mcp_src_dir} to Python path")
        return True
    else:
        logger.error(f"Error: FreeCAD MCP source directory not found at {mcp_src_dir}")
        return False

def check_is_freecad_running():
    """Check if FreeCAD is running."""
    import subprocess
    try:
        # Use ps aux instead of pgrep to check if FreeCAD is running
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, text=True)
        return 'freecad' in result.stdout.lower()
    except Exception as e:
        logger.error(f"Error checking if FreeCAD is running: {e}")
        return False

def inspect_mcp_module():
    """Inspect the MCP module to see what's available."""
    try:
        import mcp
        logger.info(f"Found MCP package: {mcp.__file__}")
        
        # Inspect the client module
        import mcp.client
        logger.info(f"MCP client module location: {mcp.client.__file__}")
        
        # Print out all the exported names in the module
        client_dir = dir(mcp.client)
        logger.info(f"Available in mcp.client: {', '.join(client_dir)}")
        
        # Inspect the session module
        import mcp.client.session
        logger.info(f"MCP session module location: {mcp.client.session.__file__}")
        session_dir = dir(mcp.client.session)
        logger.info(f"Available in mcp.client.session: {', '.join(session_dir)}")
        
        return True
    except ImportError as e:
        logger.error(f"Error importing MCP modules: {e}")
        return False

async def test_mcp_connection_async():
    """Test the connection to the FreeCAD MCP server asynchronously."""
    try:
        # Import the ClientSession class
        from mcp.client.session import ClientSession
        
        # Create a session and connect to the server
        async with ClientSession("http://localhost:5050") as session:
            logger.info("Successfully created a session with the FreeCAD MCP server")
            
            # Try to call a method on the server
            response = await session.invoke("ping")
            logger.info(f"Server response to ping: {response}")
            
            return True
    except Exception as e:
        logger.error(f"Error connecting to FreeCAD MCP server asynchronously: {e}")
        return False

def test_mcp_connection():
    """Test if we can connect to the FreeCAD MCP server."""
    if not setup_mcp_environment():
        return False
    
    if not check_is_freecad_running():
        logger.warning("FreeCAD is not running. Please start FreeCAD.")
        return False
    
    logger.info("FreeCAD is running. Checking MCP connection...")
    
    # First inspect the MCP module to help with debugging
    inspect_mcp_module()
    
    try:
        # Import the server module to check if it's properly installed
        import freecad_mcp.server
        logger.info("Successfully imported FreeCAD MCP server module")
        
        # Try the async connection
        import asyncio
        connection_result = asyncio.run(test_mcp_connection_async())
        
        if connection_result:
            logger.info("Successfully connected to FreeCAD MCP server")
            return True
        else:
            logger.error("Failed to connect to FreeCAD MCP server asynchronously")
            return False
    except ImportError as e:
        logger.error(f"Error importing modules: {e}")
        return False
    except Exception as e:
        logger.error(f"Error connecting to FreeCAD MCP server: {e}")
        logger.info("Make sure FreeCAD is running with the MCP server enabled.")
        logger.info("1. Open FreeCAD")
        logger.info("2. Go to Edit > Preferences > General > Mission Control")
        logger.info("3. Enable the MCP server on port 5050")
        logger.info("4. Click Apply and restart FreeCAD")
        logger.info("5. In the MCP Addon workbench, click the 'Start RPC Server' button")
        return False

if __name__ == "__main__":
    logger.info("Testing FreeCAD MCP connection...")
    success = test_mcp_connection()
    if success:
        logger.info("✅ Successfully connected to FreeCAD MCP server!")
        sys.exit(0)
    else:
        logger.error("❌ Failed to connect to FreeCAD MCP server.")
        sys.exit(1) 