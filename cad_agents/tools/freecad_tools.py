"""Tools for interacting with FreeCAD through MCP."""

from ..utils.mcp_utils import get_mcp_client

def get_freecad_version() -> dict:
    """Get the FreeCAD version information.
    
    Returns:
        dict: A dictionary containing the version information or an error message.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        version = client.get_version()
        return {
            "status": "success", 
            "version": version
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error getting FreeCAD version: {str(e)}"
        }

def create_box(length: float, width: float, height: float, name: str = "Box") -> dict:
    """Create a box in FreeCAD.
    
    Args:
        length (float): Length of the box
        width (float): Width of the box
        height (float): Height of the box
        name (str, optional): Name of the box. Defaults to "Box".
    
    Returns:
        dict: A dictionary with the status and information about the created box.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        # Create a new document if none exists
        docs = client.list_documents()
        if not docs:
            client.create_document("CADAgentDocument")
        
        # Create the box
        result = client.run_python_code(f"""
import FreeCAD as App
import Part
doc = App.activeDocument()
box = doc.addObject("Part::Box", "{name}")
box.Length = {length}
box.Width = {width}
box.Height = {height}
doc.recompute()
""")
        
        return {
            "status": "success",
            "message": f"Created box with dimensions {length}x{width}x{height}",
            "object_name": name
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error creating box: {str(e)}"
        }

def create_cylinder(radius: float, height: float, name: str = "Cylinder") -> dict:
    """Create a cylinder in FreeCAD.
    
    Args:
        radius (float): Radius of the cylinder
        height (float): Height of the cylinder
        name (str, optional): Name of the cylinder. Defaults to "Cylinder".
    
    Returns:
        dict: A dictionary with the status and information about the created cylinder.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        # Create a new document if none exists
        docs = client.list_documents()
        if not docs:
            client.create_document("CADAgentDocument")
        
        # Create the cylinder
        result = client.run_python_code(f"""
import FreeCAD as App
import Part
doc = App.activeDocument()
cylinder = doc.addObject("Part::Cylinder", "{name}")
cylinder.Radius = {radius}
cylinder.Height = {height}
doc.recompute()
""")
        
        return {
            "status": "success",
            "message": f"Created cylinder with radius {radius} and height {height}",
            "object_name": name
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error creating cylinder: {str(e)}"
        }

def create_sphere(radius: float, name: str = "Sphere") -> dict:
    """Create a sphere in FreeCAD.
    
    Args:
        radius (float): Radius of the sphere
        name (str, optional): Name of the sphere. Defaults to "Sphere".
    
    Returns:
        dict: A dictionary with the status and information about the created sphere.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        # Create a new document if none exists
        docs = client.list_documents()
        if not docs:
            client.create_document("CADAgentDocument")
        
        # Create the sphere
        result = client.run_python_code(f"""
import FreeCAD as App
import Part
doc = App.activeDocument()
sphere = doc.addObject("Part::Sphere", "{name}")
sphere.Radius = {radius}
doc.recompute()
""")
        
        return {
            "status": "success",
            "message": f"Created sphere with radius {radius}",
            "object_name": name
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error creating sphere: {str(e)}"
        }

def boolean_operation(obj1_name: str, obj2_name: str, operation: str = "fusion", result_name: str = "BooleanResult") -> dict:
    """Perform a boolean operation between two objects in FreeCAD.
    
    Args:
        obj1_name (str): Name of the first object
        obj2_name (str): Name of the second object
        operation (str, optional): Boolean operation type: "fusion", "cut", or "common". Defaults to "fusion".
        result_name (str, optional): Name of the result object. Defaults to "BooleanResult".
    
    Returns:
        dict: A dictionary with the status and information about the boolean operation.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    # Validate operation type
    valid_operations = ["fusion", "cut", "common"]
    if operation not in valid_operations:
        return {
            "status": "error",
            "error_message": f"Invalid operation type: {operation}. Valid types are: {', '.join(valid_operations)}"
        }
    
    try:
        # Perform the boolean operation
        result = client.run_python_code(f"""
import FreeCAD as App
import Part
doc = App.activeDocument()

# Check if objects exist
obj1 = doc.getObject("{obj1_name}")
obj2 = doc.getObject("{obj2_name}")

if obj1 is None:
    print(f"Error: Object '{obj1_name}' not found")
    result = {{"status": "error", "error_message": f"Object '{obj1_name}' not found"}}
elif obj2 is None:
    print(f"Error: Object '{obj2_name}' not found")
    result = {{"status": "error", "error_message": f"Object '{obj2_name}' not found"}}
else:
    # Create the boolean operation
    if "{operation}" == "fusion":
        boolean = doc.addObject("Part::Fuse", "{result_name}")
    elif "{operation}" == "cut":
        boolean = doc.addObject("Part::Cut", "{result_name}")
    elif "{operation}" == "common":
        boolean = doc.addObject("Part::Common", "{result_name}")
    
    boolean.Base = obj1
    boolean.Tool = obj2
    doc.recompute()
    result = {{"status": "success", "object_name": "{result_name}"}}

print(f"Boolean result: {{result}}")
""")
        
        # Check if the operation was successful
        if "success" in result.get("output", ""):
            return {
                "status": "success",
                "message": f"Performed {operation} operation between {obj1_name} and {obj2_name}",
                "object_name": result_name
            }
        else:
            # Extract error message from output
            error_msg = result.get("output", "Unknown error")
            return {
                "status": "error",
                "error_message": f"Error performing boolean operation: {error_msg}"
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error performing boolean operation: {str(e)}"
        }

def set_object_placement(obj_name: str, x: float = 0, y: float = 0, z: float = 0, 
                         axis_x: float = 0, axis_y: float = 0, axis_z: float = 1, 
                         angle: float = 0) -> dict:
    """Set the placement (position and rotation) of an object in FreeCAD.
    
    Args:
        obj_name (str): Name of the object to position
        x (float, optional): X coordinate. Defaults to 0.
        y (float, optional): Y coordinate. Defaults to 0.
        z (float, optional): Z coordinate. Defaults to 0.
        axis_x (float, optional): X component of rotation axis. Defaults to 0.
        axis_y (float, optional): Y component of rotation axis. Defaults to 0.
        axis_z (float, optional): Z component of rotation axis. Defaults to 1.
        angle (float, optional): Rotation angle in degrees. Defaults to 0.
    
    Returns:
        dict: A dictionary with the status and information about the placement operation.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        # Set the object placement
        result = client.run_python_code(f"""
import FreeCAD as App
import Part
from FreeCAD import Base
doc = App.activeDocument()

# Check if object exists
obj = doc.getObject("{obj_name}")

if obj is None:
    print(f"Error: Object '{obj_name}' not found")
    result = {{"status": "error", "error_message": f"Object '{obj_name}' not found"}}
else:
    # Create a placement with position and rotation
    position = Base.Vector({x}, {y}, {z})
    rotation_axis = Base.Vector({axis_x}, {axis_y}, {axis_z})
    rotation = Base.Rotation(rotation_axis, {angle})
    placement = Base.Placement(position, rotation)
    
    # Apply the placement to the object
    obj.Placement = placement
    doc.recompute()
    result = {{"status": "success"}}

print(f"Placement result: {{result}}")
""")
        
        # Check if the operation was successful
        if "success" in result.get("output", ""):
            return {
                "status": "success",
                "message": f"Set placement of {obj_name} to position ({x}, {y}, {z}) with rotation ({axis_x}, {axis_y}, {axis_z}, {angle})"
            }
        else:
            # Extract error message from output
            error_msg = result.get("output", "Unknown error")
            return {
                "status": "error",
                "error_message": f"Error setting object placement: {error_msg}"
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error setting object placement: {str(e)}"
        }

def list_objects() -> dict:
    """List all objects in the active FreeCAD document.
    
    Returns:
        dict: A dictionary containing the list of objects or an error message.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        # Check if any document exists
        docs = client.list_documents()
        if not docs:
            return {
                "status": "success",
                "objects": [],
                "message": "No documents found."
            }
        
        # Get objects from active document
        result = client.run_python_code("""
import FreeCAD as App
doc = App.activeDocument()
objects = [obj.Name for obj in doc.Objects]
print(objects)
""")
        
        # Parse the output to get the list of objects
        # Assuming the run_python_code returns the printed output
        if "success" in result and result["success"]:
            objects_str = result.get("output", "[]")
            try:
                # Clean up the output and evaluate it as a Python list
                objects_str = objects_str.strip()
                objects = eval(objects_str)
                return {
                    "status": "success",
                    "objects": objects
                }
            except:
                return {
                    "status": "error",
                    "error_message": f"Failed to parse object list: {objects_str}"
                }
        else:
            return {
                "status": "error",
                "error_message": "Failed to run Python code in FreeCAD"
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error listing objects: {str(e)}"
        }

def save_document(filename: str) -> dict:
    """Save the active FreeCAD document.
    
    Args:
        filename (str): Filename to save the document as (without extension)
    
    Returns:
        dict: A dictionary with the status and information about the saved document.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        # Check if any document exists
        docs = client.list_documents()
        if not docs:
            return {
                "status": "error",
                "error_message": "No document found to save."
            }
        
        # Ensure the filename has the correct extension
        if not filename.endswith(".FCStd"):
            filename = f"{filename}.FCStd"
        
        # Save the document
        result = client.run_python_code(f"""
import FreeCAD as App
doc = App.activeDocument()
doc.saveAs("{filename}")
print("Document saved as {filename}")
""")
        
        return {
            "status": "success",
            "message": f"Document saved as {filename}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error saving document: {str(e)}"
        } 