#!/usr/bin/env python3
"""Advanced test script to explore FreeCAD's capabilities through the RPC interface."""

import sys
import logging
import time
import xmlrpc.client
import subprocess
import json
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

def execute_freecad_code(rpc_server, code):
    """Execute arbitrary Python code in FreeCAD."""
    try:
        logger.info(f"Executing code: {code.strip()}")
        result = rpc_server.execute_code(code)
        if result["success"]:
            logger.info("Code execution successful")
            return True
        else:
            logger.error(f"Code execution failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        logger.error(f"Error executing code: {e}")
        return False

def create_complex_model(rpc_server):
    """Create a more complex model in FreeCAD with boolean operations and styling."""
    try:
        # Create a new document
        logger.info("Creating a new document...")
        doc_result = rpc_server.create_document("ComplexTest")
        if not doc_result["success"]:
            logger.error(f"Failed to create document: {doc_result.get('error', 'Unknown error')}")
            return False
        
        logger.info(f"Document '{doc_result['document_name']}' created successfully.")
        
        # Create a base cylinder
        logger.info("Creating base cylinder...")
        base_cylinder_data = {
            "Name": "BaseCylinder",
            "Type": "Part::Cylinder",
            "Properties": {
                "Radius": 20.0,
                "Height": 60.0,
                "Placement": {
                    "Base": {"x": 0, "y": 0, "z": 0},
                    "Rotation": {"Axis": {"x": 0, "y": 0, "z": 1}, "Angle": 0}
                },
                "ViewObject": {
                    "ShapeColor": [0.8, 0.2, 0.2, 1.0]  # Red color with alpha
                }
            }
        }
        
        base_result = rpc_server.create_object("ComplexTest", base_cylinder_data)
        if not base_result["success"]:
            logger.error(f"Failed to create base cylinder: {base_result.get('error', 'Unknown error')}")
            return False
        
        logger.info(f"Base cylinder '{base_result['object_name']}' created successfully.")
        
        # Create a cutting box
        logger.info("Creating cutting box...")
        cutting_box_data = {
            "Name": "CuttingBox",
            "Type": "Part::Box",
            "Properties": {
                "Length": 50.0,
                "Width": 20.0,
                "Height": 20.0,
                "Placement": {
                    "Base": {"x": -25, "y": -10, "z": 20},
                    "Rotation": {"Axis": {"x": 0, "y": 0, "z": 1}, "Angle": 0}
                },
                "ViewObject": {
                    "ShapeColor": [0.2, 0.2, 0.8, 1.0]  # Blue color with alpha
                }
            }
        }
        
        cutting_result = rpc_server.create_object("ComplexTest", cutting_box_data)
        if not cutting_result["success"]:
            logger.error(f"Failed to create cutting box: {cutting_result.get('error', 'Unknown error')}")
            return False
        
        logger.info(f"Cutting box '{cutting_result['object_name']}' created successfully.")
        
        # Create a sphere to be fused to the base
        logger.info("Creating sphere...")
        sphere_data = {
            "Name": "AdditiveSphere",
            "Type": "Part::Sphere",
            "Properties": {
                "Radius": 15.0,
                "Placement": {
                    "Base": {"x": 0, "y": 30, "z": 30},
                    "Rotation": {"Axis": {"x": 0, "y": 0, "z": 1}, "Angle": 0}
                },
                "ViewObject": {
                    "ShapeColor": [0.2, 0.8, 0.2, 1.0]  # Green color with alpha
                }
            }
        }
        
        sphere_result = rpc_server.create_object("ComplexTest", sphere_data)
        if not sphere_result["success"]:
            logger.error(f"Failed to create sphere: {sphere_result.get('error', 'Unknown error')}")
            return False
        
        logger.info(f"Sphere '{sphere_result['object_name']}' created successfully.")
        
        # Create a cut operation (cylinder - box)
        logger.info("Performing cut operation (cylinder - box)...")
        
        # Use execute_code to perform boolean operations since they're not directly exposed via the RPC API
        cut_code = """
import FreeCAD
doc = FreeCAD.getDocument("ComplexTest")
cut = doc.addObject("Part::Cut", "CylinderCut")
cut.Base = doc.BaseCylinder
cut.Tool = doc.CuttingBox
cut.ViewObject.ShapeColor = (0.8, 0.5, 0.2, 1.0) # Orange
doc.recompute()
        """
        
        if not execute_freecad_code(rpc_server, cut_code):
            return False
        
        logger.info("Cut operation completed successfully.")
        
        # Create a fusion operation (cut result + sphere)
        logger.info("Performing fusion operation (cut result + sphere)...")
        
        fusion_code = """
import FreeCAD
doc = FreeCAD.getDocument("ComplexTest")
fusion = doc.addObject("Part::Fuse", "FinalShape")
fusion.Base = doc.CylinderCut
fusion.Tool = doc.AdditiveSphere
fusion.ViewObject.ShapeColor = (0.8, 0.8, 0.0, 1.0) # Yellow
doc.recompute()
        """
        
        if not execute_freecad_code(rpc_server, fusion_code):
            return False
        
        logger.info("Fusion operation completed successfully.")
        
        # Add fillets to the edges (more advanced operation)
        logger.info("Adding fillets to the final shape...")
        
        fillet_code = """
import FreeCAD
import Part
doc = FreeCAD.getDocument("ComplexTest")

# Create a fillet on the final shape
fillet = doc.addObject("Part::Fillet", "FilletedShape")
fillet.Base = doc.FinalShape

# Get all edges for filleting
edges = []
for i, edge in enumerate(doc.FinalShape.Shape.Edges):
    edges.append((i+1, 3.0, 3.0))  # (edge_index, radius1, radius2)

fillet.Edges = edges
doc.recompute()

# Hide original objects
doc.BaseCylinder.ViewObject.Visibility = False
doc.CuttingBox.ViewObject.Visibility = False
doc.AdditiveSphere.ViewObject.Visibility = False
doc.CylinderCut.ViewObject.Visibility = False
doc.FinalShape.ViewObject.Visibility = False

# Set the fillet color
fillet.ViewObject.ShapeColor = (0.9, 0.5, 0.9, 1.0)  # Purple
        """
        
        if not execute_freecad_code(rpc_server, fillet_code):
            # Fillets might fail on complex shapes, but we can continue
            logger.warning("Fillet operation failed, but continuing with the test.")
        else:
            logger.info("Fillet operation completed successfully.")
        
        # Create a polar pattern (advanced feature)
        logger.info("Creating a polar pattern of a small cylinder...")
        
        pattern_code = """
import FreeCAD
import Part
doc = FreeCAD.getDocument("ComplexTest")

# Create a small cylinder to be patterned
small_cyl = doc.addObject("Part::Cylinder", "PatternBase")
small_cyl.Radius = 3.0
small_cyl.Height = 10.0
small_cyl.Placement = FreeCAD.Placement(
    FreeCAD.Vector(40, 0, 0),
    FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), 90)
)
small_cyl.ViewObject.ShapeColor = (1.0, 0.0, 0.0, 1.0)  # Pure red

doc.recompute()

# Function to create a circular pattern
def create_circular_pattern(obj, count):
    shapes = []
    for i in range(count):
        angle = i * (360.0 / count)
        placement = FreeCAD.Placement()
        placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), angle)
        copy = obj.Shape.copy()
        copy.transformShape(placement.toMatrix())
        shapes.append(copy)
    
    compound = Part.makeCompound(shapes)
    pattern = doc.addObject("Part::Feature", "PolarPattern")
    pattern.Shape = compound
    pattern.ViewObject.ShapeColor = (1.0, 0.0, 0.0, 1.0)  # Pure red
    return pattern

# Create a pattern with 8 instances
create_circular_pattern(small_cyl, 8)
doc.recompute()

# Hide the original
small_cyl.ViewObject.Visibility = False
        """
        
        if not execute_freecad_code(rpc_server, pattern_code):
            # Pattern might fail, but we can continue
            logger.warning("Polar pattern operation failed, but continuing with the test.")
        else:
            logger.info("Polar pattern created successfully.")
        
        # List all objects in the document
        objects = rpc_server.get_objects("ComplexTest")
        logger.info(f"Objects in document: {[obj['Name'] for obj in objects]}")
        
        # Take a screenshot of the final result
        screenshot = rpc_server.get_active_screenshot("Isometric")
        if screenshot:
            logger.info("Screenshot captured successfully.")
        
        logger.info("Complex model creation complete!")
        return True
    
    except Exception as e:
        logger.error(f"Error creating complex model: {e}")
        return False

if __name__ == "__main__":
    logger.info("Testing FreeCAD advanced model creation...")
    rpc_server = test_freecad_rpc_connection()
    
    if rpc_server:
        success = create_complex_model(rpc_server)
        if success:
            logger.info("✅ Successfully created a complex model in FreeCAD!")
            sys.exit(0)
        else:
            logger.error("❌ Failed to create a complex model in FreeCAD.")
            sys.exit(1)
    else:
        logger.error("❌ Failed to connect to FreeCAD RPC server.")
        sys.exit(1) 