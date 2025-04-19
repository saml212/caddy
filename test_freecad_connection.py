#!/usr/bin/env python3
"""Script to test the connection to both FreeCAD RPC server and MCP server."""

import sys
import logging
import xmlrpc.client
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def check_is_freecad_running():
    """Check if FreeCAD is running."""
    try:
        # Use ps aux to check if FreeCAD is running
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, text=True)
        return 'freecad' in result.stdout.lower()
    except Exception as e:
        logger.error(f"Error checking if FreeCAD is running: {e}")
        return False

def test_freecad_rpc_connection():
    """Test connection to the FreeCAD RPC server on port 9875."""
    if not check_is_freecad_running():
        logger.warning("FreeCAD is not running. Please start FreeCAD.")
        return False
    
    try:
        # Try to connect to the FreeCAD RPC server
        rpc_server = xmlrpc.client.ServerProxy("http://localhost:9875", allow_none=True)
        
        # Test the connection with a simple ping
        result = rpc_server.ping()
        if result:
            logger.info("✅ Successfully connected to FreeCAD RPC server on port 9875")
            
            # Get the list of documents
            documents = rpc_server.list_documents()
            logger.info(f"FreeCAD documents: {documents}")
            
            return True
        else:
            logger.error("Failed to ping FreeCAD RPC server")
            return False
    except Exception as e:
        logger.error(f"Error connecting to FreeCAD RPC server: {e}")
        logger.info("Make sure the RPC server is started in FreeCAD:")
        logger.info("1. In FreeCAD, select the 'MCP Addon' workbench")
        logger.info("2. Click the 'Start RPC Server' button in the toolbar")
        return False

def check_mcp_server_running():
    """Check if the MCP server is running on port 5050."""
    import socket
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(('localhost', 5050))
        s.close()
        
        if result == 0:
            logger.info("✅ MCP server is running on port 5050")
            return True
        else:
            logger.warning("❌ MCP server is not running on port 5050")
            return False
    except Exception as e:
        logger.error(f"Error checking if MCP server is running: {e}")
        return False

def test_connections():
    """Test both FreeCAD RPC and MCP connections."""
    # Test FreeCAD RPC connection
    freecad_rpc_result = test_freecad_rpc_connection()
    
    # Test MCP server
    mcp_server_result = check_mcp_server_running()
    
    if freecad_rpc_result and mcp_server_result:
        logger.info("✅ All connections successful!")
        return True
    elif freecad_rpc_result and not mcp_server_result:
        logger.warning("⚠️ FreeCAD RPC connection successful, but MCP server is not running.")
        logger.info("You need to start the MCP server:")
        logger.info("1. Make sure the FreeCADMCP addon is installed in FreeCAD")
        logger.info("2. In FreeCAD, go to Edit > Preferences > General > Mission Control")
        logger.info("3. Enable the MCP server on port 5050")
        logger.info("4. Click Apply and restart FreeCAD")
        return False
    elif not freecad_rpc_result and mcp_server_result:
        logger.warning("⚠️ MCP server is running, but FreeCAD RPC connection failed.")
        return False
    else:
        logger.error("❌ All connections failed.")
        return False

if __name__ == "__main__":
    logger.info("Testing FreeCAD and MCP connections...")
    success = test_connections()
    if success:
        logger.info("✅ Successfully connected to both FreeCAD RPC and MCP servers!")
        sys.exit(0)
    else:
        logger.error("❌ Failed to connect to one or both servers.")
        sys.exit(1) 