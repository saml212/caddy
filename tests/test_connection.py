#!/usr/bin/env python3
"""Simple script to test connection to FreeCAD RPC server on port 9876."""

import sys
import logging
import xmlrpc.client
import subprocess

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
    """Test connection to the FreeCAD RPC server on port 9876."""
    if not check_is_freecad_running():
        logger.warning("FreeCAD is not running. Please start FreeCAD.")
        return False
    
    try:
        # Try to connect to the FreeCAD RPC server
        logger.info("Connecting to FreeCAD RPC server on port 9876...")
        rpc_server = xmlrpc.client.ServerProxy("http://localhost:9876", allow_none=True)
        
        # Test the connection with a simple ping
        result = rpc_server.ping()
        if result:
            logger.info("✅ Successfully connected to FreeCAD RPC server on port 9876")
            
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

if __name__ == "__main__":
    logger.info("Testing FreeCAD RPC connection...")
    success = test_freecad_rpc_connection()
    if success:
        logger.info("✅ Successfully connected to FreeCAD RPC server!")
        sys.exit(0)
    else:
        logger.error("❌ Failed to connect to FreeCAD RPC server.")
        sys.exit(1) 