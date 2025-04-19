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