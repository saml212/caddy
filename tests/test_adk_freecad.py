#!/usr/bin/env python3
"""Test script to verify if the Google ADK can use the FreeCAD-MCP server."""

import os
import sys
import logging
import asyncio
from pathlib import Path
from dotenv import load_dotenv

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

async def run_freecad_mcp_server():
    """Run the FreeCAD MCP server as a subprocess."""
    try:
        # Get the absolute path to the freecad-mcp module
        root_dir = Path(__file__).parent
        mcp_src_dir = root_dir / "freecad-mcp" / "src"
        
        if not mcp_src_dir.exists():
            logger.error(f"FreeCAD MCP source directory not found at {mcp_src_dir}")
            return None
        
        # Set up environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{str(mcp_src_dir)}:{env.get('PYTHONPATH', '')}"
        
        # Start the FreeCAD MCP server
        logger.info("Starting the FreeCAD MCP server...")
        process = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "freecad_mcp.server",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )
        
        logger.info(f"FreeCAD MCP server started with PID {process.pid}")
        return process
    except Exception as e:
        logger.error(f"Error starting FreeCAD MCP server: {e}")
        return None

async def test_adk_with_freecad():
    """Test the Google ADK with FreeCAD MCP."""
    # Load environment variables
    load_dotenv()
    
    # Set up MCP environment
    if not setup_mcp_environment():
        logger.error("Failed to set up MCP environment")
        return False
    
    # Check if required environment variables are set
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
    
    try:
        # Start the FreeCAD MCP server
        server_process = await run_freecad_mcp_server()
        if not server_process:
            logger.error("Failed to start FreeCAD MCP server")
            return False
        
        try:
            # Import Google ADK modules
            from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
            
            # Connect to the FreeCAD MCP server using ADK's MCPToolset
            logger.info("Connecting to FreeCAD MCP server using ADK's MCPToolset...")
            
            # Get the absolute path to the freecad-mcp module
            root_dir = Path(__file__).parent
            mcp_src_dir = root_dir / "freecad-mcp" / "src"
            
            # Set up server parameters
            server_params = StdioServerParameters(
                command=sys.executable,
                args=["-m", "freecad_mcp.server"],
                env={"PYTHONPATH": f"{str(mcp_src_dir)}:{os.getenv('PYTHONPATH', '')}"}
            )
            
            # Connect to the server
            tools, exit_stack = await MCPToolset.from_server(connection_params=server_params)
            
            if tools and exit_stack:
                tool_names = [tool.name for tool in tools]
                logger.info(f"Successfully connected to FreeCAD MCP server. Found tools: {tool_names}")
                
                # Make sure we clean up properly
                await exit_stack.aclose()
                logger.info("MCP connection test passed")
                return True
            else:
                logger.warning("Could not connect to FreeCAD MCP server. Make sure it's running.")
                return False
        except Exception as e:
            logger.error(f"Error testing MCP connection: {e}")
            return False
        finally:
            # Terminate the server process
            if server_process:
                server_process.terminate()
                await server_process.wait()
                logger.info("FreeCAD MCP server stopped")
    except Exception as e:
        logger.error(f"Error in test_adk_with_freecad: {e}")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(test_adk_with_freecad())
        if result:
            logger.info("✅ Test passed! Google ADK can successfully use the FreeCAD-MCP server.")
            sys.exit(0)
        else:
            logger.error("❌ Test failed. Check the logs above for details.")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error running test: {e}")
        sys.exit(1) 