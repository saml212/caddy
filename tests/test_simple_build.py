#!/usr/bin/env python3
"""Test script to build a simple object in FreeCAD using the MCP connection."""

import sys
import logging
import time
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
            return rpc_server
        else:
            logger.error("Failed to ping FreeCAD RPC server")
            return None
    except Exception as e:
        logger.error(f"Error connecting to FreeCAD RPC server: {e}")
        logger.info("Make sure the RPC server is started in FreeCAD:")
        logger.info("1. In FreeCAD, select the 'MCP Addon' workbench")
        logger.info("2. Click the 'Start RPC Server' button in the toolbar")
        return None

def create_simple_model(rpc_server):
    """Create a simple model in FreeCAD."""
    try:
        # Create a new document
        logger.info("Creating a new document...")
        doc_result = rpc_server.create_document("SimpleTest")
        if not doc_result["success"]:
            logger.error(f"Failed to create document: {doc_result.get('error', 'Unknown error')}")
            return False
        
        logger.info(f"Document '{doc_result['document_name']}' created successfully.")
        
        # Create a box
        logger.info("Creating a box...")
        box_data = {
            "Name": "SimpleBox",
            "Type": "Part::Box",
            "Properties": {
                "Length": 50.0,
                "Width": 30.0,
                "Height": 20.0,
                "Placement": {
                    "Base": {"x": 0, "y": 0, "z": 0},
                    "Rotation": {"Axis": {"x": 0, "y": 0, "z": 1}, "Angle": 0}
                }
            }
        }
        
        box_result = rpc_server.create_object("SimpleTest", box_data)
        if not box_result["success"]:
            logger.error(f"Failed to create box: {box_result.get('error', 'Unknown error')}")
            return False
        
        logger.info(f"Box '{box_result['object_name']}' created successfully.")
        
        # Create a cylinder
        logger.info("Creating a cylinder...")
        cylinder_data = {
            "Name": "SimpleCylinder",
            "Type": "Part::Cylinder",
            "Properties": {
                "Radius": 10.0,
                "Height": 40.0,
                "Placement": {
                    "Base": {"x": 60, "y": 20, "z": 0},
                    "Rotation": {"Axis": {"x": 0, "y": 0, "z": 1}, "Angle": 0}
                }
            }
        }
        
        cylinder_result = rpc_server.create_object("SimpleTest", cylinder_data)
        if not cylinder_result["success"]:
            logger.error(f"Failed to create cylinder: {cylinder_result.get('error', 'Unknown error')}")
            return False
        
        logger.info(f"Cylinder '{cylinder_result['object_name']}' created successfully.")
        
        # List all objects in the document
        objects = rpc_server.get_objects("SimpleTest")
        logger.info(f"Objects in document: {[obj['Name'] for obj in objects]}")
        
        logger.info("Simple model creation complete!")
        return True
    
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        return False

if __name__ == "__main__":
    logger.info("Testing FreeCAD simple model creation...")
    rpc_server = test_freecad_rpc_connection()
    
    if rpc_server:
        success = create_simple_model(rpc_server)
        if success:
            logger.info("✅ Successfully created a simple model in FreeCAD!")
            sys.exit(0)
        else:
            logger.error("❌ Failed to create a simple model in FreeCAD.")
            sys.exit(1)
    else:
        logger.error("❌ Failed to connect to FreeCAD RPC server.")
        sys.exit(1) 