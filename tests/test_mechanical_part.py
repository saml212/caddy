#!/usr/bin/env python3
"""Test script to build a realistic mechanical component in FreeCAD."""

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

def execute_freecad_code(rpc_server, code):
    """Execute arbitrary Python code in FreeCAD."""
    try:
        logger.info(f"Executing code block...")
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

def create_threaded_bushing(rpc_server):
    """Create a threaded bushing component in FreeCAD."""
    try:
        # Create a new document
        logger.info("Creating a new document...")
        doc_result = rpc_server.create_document("ThreadedBushing")
        if not doc_result["success"]:
            logger.error(f"Failed to create document: {doc_result.get('error', 'Unknown error')}")
            return False
        
        logger.info(f"Document '{doc_result['document_name']}' created successfully.")
        
        # First, let's create the main body of the bushing using Part Workbench
        logger.info("Creating the main body of the bushing...")
        
        # Create a cylinder for the outer body
        outer_body_code = """
import FreeCAD
import Part
from FreeCAD import Base

# Get the active document
doc = FreeCAD.getDocument("ThreadedBushing")

# Create outer cylinder
outer_cylinder = doc.addObject("Part::Cylinder", "OuterBody")
outer_cylinder.Radius = 15.0
outer_cylinder.Height = 40.0
outer_cylinder.Placement = FreeCAD.Placement(Base.Vector(0, 0, 0), Base.Rotation(0, 0, 0, 1))
outer_cylinder.ViewObject.ShapeColor = (0.7, 0.7, 0.7, 1.0)  # Gray color

doc.recompute()
        """
        
        if not execute_freecad_code(rpc_server, outer_body_code):
            return False
        
        logger.info("Outer body created successfully.")
        
        # Create a cylinder for the inner hole
        inner_hole_code = """
import FreeCAD
import Part

# Get the active document
doc = FreeCAD.getDocument("ThreadedBushing")

# Create inner cylinder for the hole
inner_cylinder = doc.addObject("Part::Cylinder", "InnerHole")
inner_cylinder.Radius = 8.0
inner_cylinder.Height = 42.0  # Slightly longer for clean boolean operation
inner_cylinder.Placement = FreeCAD.Placement(
    FreeCAD.Vector(0, 0, -1),  # Offset to ensure it extends beyond both ends
    FreeCAD.Rotation(0, 0, 0, 1)
)

doc.recompute()
        """
        
        if not execute_freecad_code(rpc_server, inner_hole_code):
            return False
        
        logger.info("Inner hole created successfully.")
        
        # Create the flange at one end
        flange_code = """
import FreeCAD
import Part

# Get the active document
doc = FreeCAD.getDocument("ThreadedBushing")

# Create flange (a larger cylinder at one end)
flange = doc.addObject("Part::Cylinder", "Flange")
flange.Radius = 25.0
flange.Height = 5.0
flange.Placement = FreeCAD.Placement(
    FreeCAD.Vector(0, 0, 35),  # Place it at the top of the main cylinder
    FreeCAD.Rotation(0, 0, 0, 1)
)

doc.recompute()
        """
        
        if not execute_freecad_code(rpc_server, flange_code):
            return False
        
        logger.info("Flange created successfully.")
        
        # Create the mounting holes in the flange
        mounting_holes_code = """
import FreeCAD
import Part
import math

# Get the active document
doc = FreeCAD.getDocument("ThreadedBushing")

# Create 4 mounting holes in the flange
hole_radius = 5.0
hole_distance_from_center = 18.0

for i in range(4):
    angle = i * math.pi / 2  # Evenly space 4 holes
    x = hole_distance_from_center * math.cos(angle)
    y = hole_distance_from_center * math.sin(angle)
    
    mounting_hole = doc.addObject("Part::Cylinder", f"MountingHole_{i+1}")
    mounting_hole.Radius = 3.0
    mounting_hole.Height = 8.0
    mounting_hole.Placement = FreeCAD.Placement(
        FreeCAD.Vector(x, y, 34),  # Position on the flange, slightly below its top
        FreeCAD.Rotation(0, 0, 0, 1)
    )

doc.recompute()
        """
        
        if not execute_freecad_code(rpc_server, mounting_holes_code):
            return False
        
        logger.info("Mounting holes created successfully.")
        
        # Create hexagonal feature on the outer surface for a wrench
        hex_feature_code = """
import FreeCAD
import Part

# Get the active document
doc = FreeCAD.getDocument("ThreadedBushing")

# Create a hexagonal prism for wrench grip
hex_radius = 18.0  # Radius of the circumscribed circle
hex_height = 10.0

# Create a hexagonal face
polygon = []
for i in range(6):
    angle = i * 2 * math.pi / 6
    polygon.append(FreeCAD.Vector(hex_radius * math.cos(angle), 
                                 hex_radius * math.sin(angle), 
                                 0))

# Create a face from the polygon
hex_face = Part.makePolygon(polygon + [polygon[0]])
hex_face = Part.Face(hex_face)

# Extrude the face
hex_prism = hex_face.extrude(FreeCAD.Vector(0, 0, hex_height))

# Create a Part Feature
hex_part = doc.addObject("Part::Feature", "HexGrip")
hex_part.Shape = hex_prism
hex_part.Placement = FreeCAD.Placement(
    FreeCAD.Vector(0, 0, 15),  # Place in the middle of the body
    FreeCAD.Rotation(0, 0, 0, 1)
)

doc.recompute()
        """
        
        if not execute_freecad_code(rpc_server, hex_feature_code):
            return False
        
        logger.info("Hexagonal grip feature created successfully.")
        
        # Perform boolean operations to create the final part
        boolean_ops_code = """
import FreeCAD
import Part

# Get the active document
doc = FreeCAD.getDocument("ThreadedBushing")

# First, fuse the main body with the flange
body_fusion = doc.addObject("Part::Fuse", "BodyWithFlange")
body_fusion.Base = doc.OuterBody
body_fusion.Tool = doc.Flange
doc.recompute()

# Now union with the hex grip
hex_fusion = doc.addObject("Part::Fuse", "BodyWithHex")
hex_fusion.Base = doc.BodyWithFlange
hex_fusion.Tool = doc.HexGrip
doc.recompute()

# Cut the inner hole
hole_cut = doc.addObject("Part::Cut", "BodyWithHole")
hole_cut.Base = doc.BodyWithHex
hole_cut.Tool = doc.InnerHole
doc.recompute()

# Cut the mounting holes
final_part = doc.addObject("Part::MultiFuse", "FinalPart")
final_part.Shapes = [doc.BodyWithHole]

for i in range(4):
    mounting_hole_name = f"MountingHole_{i+1}"
    mounting_hole_obj = doc.getObject(mounting_hole_name)
    
    mounting_cut = doc.addObject("Part::Cut", f"Cut_{i+1}")
    mounting_cut.Base = final_part if i == 0 else doc.getObject(f"Cut_{i}")
    mounting_cut.Tool = mounting_hole_obj
    doc.recompute()
    
    if i == 3:
        final_part = mounting_cut

# Create thread on the inner hole using Part Design workbench
# This is just a visual approximation for demonstration
thread_code = "import FreeCAD\\nimport Part\\n\\n"
thread_code += "doc = FreeCAD.getDocument(\\"ThreadedBushing\\")\\n\\n"
thread_code += "thread_radius = 8.0\\n"
thread_code += "thread_height = 30.0\\n"
thread_code += "thread_pitch = 1.5\\n"
thread_code += "thread_depth = 0.5\\n"
thread_code += "\\n"
thread_code += "# Create a helix\\n"
thread_code += "helix = Part.makeHelix(thread_pitch, thread_height, thread_radius)\\n"
thread_code += "\\n"
thread_code += "# Create a profile for the thread\\n"
thread_code += "profile = Part.makePolygon([\\n"
thread_code += "    FreeCAD.Vector(0, 0, 0),\\n"
thread_code += "    FreeCAD.Vector(thread_depth, thread_depth, 0),\\n"
thread_code += "    FreeCAD.Vector(0, thread_depth*2, 0),\\n"
thread_code += "    FreeCAD.Vector(0, 0, 0)\\n"
thread_code += "])\\n"
thread_code += "\\n"
thread_code += "# Sweep the profile along the helix\\n"
thread_code += "thread_shape = Part.Wire(profile).makePipeShell([helix], True, False)\\n"
thread_code += "\\n"
thread_code += "# Create a Part Feature\\n"
thread_code += "thread_part = doc.addObject(\\"Part::Feature\\", \\"ThreadFeature\\")\\n"
thread_code += "thread_part.Shape = thread_shape\\n"
thread_code += "thread_part.Placement = FreeCAD.Placement(\\n"
thread_code += "    FreeCAD.Vector(0, 0, 5),  # Start the thread a bit above the bottom\\n"
thread_code += "    FreeCAD.Rotation(0, 0, 0, 1)\\n"
thread_code += ")\\n"
thread_code += "thread_part.ViewObject.ShapeColor = (0.1, 0.1, 0.1, 1.0)  # Dark color for thread\\n"
thread_code += "\\n"
thread_code += "# Hide all the construction objects, show only the final part\\n"
thread_code += "for obj in doc.Objects:\\n"
thread_code += "    if obj.Name != \\"ThreadFeature\\" and obj.Name != \\"Cut_3\\":\\n"
thread_code += "        obj.ViewObject.Visibility = False\\n"
thread_code += "\\n"
thread_code += "doc.recompute()\\n"

# Save thread code to a file for inspection
with open("thread_code.py", "w") as f:
    f.write(thread_code)

# Now execute the thread code
exec(thread_code)
        """
        
        if not execute_freecad_code(rpc_server, boolean_ops_code):
            return False
        
        logger.info("Boolean operations completed successfully.")
        
        # Add chamfers and fillets to the edges for a more realistic look
        finishing_code = """
import FreeCAD
import Part

# Get the active document
doc = FreeCAD.getDocument("ThreadedBushing")

# Get the final part
final_part = doc.getObject("Cut_3")

# Add fillets to the outer edges
fillets = doc.addObject("Part::Fillet", "FilletedPart")
fillets.Base = final_part

# Get edges of the base shape
edges = []
for i, edge in enumerate(final_part.Shape.Edges):
    # Only add fillets to certain edges (simplified example)
    if edge.Length > 20:  # This is a simplified way to select certain edges
        edges.append((i+1, 1.0, 1.0))  # (EdgeIndex, Radius1, Radius2)

fillets.Edges = edges
doc.recompute()

# Hide all the objects except the final part and thread
for obj in doc.Objects:
    if obj.Name != "FilletedPart" and obj.Name != "ThreadFeature":
        obj.ViewObject.Visibility = False

# Set material appearance for a more realistic look
fillets.ViewObject.ShapeColor = (0.8, 0.8, 0.8, 1.0)  # Silver color for metal appearance

doc.recompute()
        """
        
        if not execute_freecad_code(rpc_server, finishing_code):
            # Fillets might fail, but we can continue
            logger.warning("Finishing operations failed, but continuing with the test.")
        else:
            logger.info("Finishing operations completed successfully.")
        
        # List all objects in the document
        objects = rpc_server.get_objects("ThreadedBushing")
        logger.info(f"Objects in document: {[obj['Name'] for obj in objects]}")
        
        # Take a screenshot of the final result
        screenshot = rpc_server.get_active_screenshot("Isometric")
        if screenshot:
            logger.info("Screenshot captured successfully.")
        
        # Get a different view
        rpc_server.get_active_screenshot("Right") 
        logger.info("Right view captured.")
        
        # Get a third view
        rpc_server.get_active_screenshot("Top")
        logger.info("Top view captured.")
        
        logger.info("Threaded bushing creation complete!")
        return True
    
    except Exception as e:
        logger.error(f"Error creating threaded bushing: {e}")
        return False

if __name__ == "__main__":
    logger.info("Testing FreeCAD - Creating a threaded bushing...")
    rpc_server = test_freecad_rpc_connection()
    
    if rpc_server:
        success = create_threaded_bushing(rpc_server)
        if success:
            logger.info("✅ Successfully created a threaded bushing in FreeCAD!")
            sys.exit(0)
        else:
            logger.error("❌ Failed to create a threaded bushing in FreeCAD.")
            sys.exit(1)
    else:
        logger.error("❌ Failed to connect to FreeCAD RPC server.")
        sys.exit(1) 