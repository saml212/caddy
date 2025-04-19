"""Tools for analyzing FreeCAD models."""

from ..utils.mcp_utils import get_mcp_client

def calculate_volume(obj_name: str) -> dict:
    """Calculate the volume of a FreeCAD object.
    
    Args:
        obj_name (str): Name of the object
    
    Returns:
        dict: A dictionary with the status and volume information.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        # Calculate volume
        result = client.run_python_code(f"""
import FreeCAD as App
doc = App.activeDocument()

# Check if object exists
obj = doc.getObject("{obj_name}")

if obj is None:
    print(f"Error: Object '{obj_name}' not found")
    result = {{"status": "error", "error_message": f"Object '{obj_name}' not found"}}
else:
    # Get the shape and calculate volume
    try:
        # Check if object has a Shape
        if hasattr(obj, "Shape"):
            volume = obj.Shape.Volume
            print(f"Volume calculation: {{'status': 'success', 'volume': {volume}, 'unit': 'mm³'}}")
            result = {{"status": "success", "volume": {volume}, "unit": "mm³"}}
        else:
            print(f"Error: Object '{obj_name}' has no Shape property")
            result = {{"status": "error", "error_message": f"Object '{obj_name}' has no Shape property"}}
    except Exception as e:
        print(f"Error calculating volume: {{str(e)}}")
        result = {{"status": "error", "error_message": f"Error calculating volume: {{str(e)}}"}}
""")
        
        # Check if the operation was successful
        if "success" in result.get("output", ""):
            # Extract volume from output
            import re
            match = re.search(r"'volume': (\d+\.?\d*)", result.get("output", ""))
            if match:
                volume = float(match.group(1))
                return {
                    "status": "success",
                    "volume": volume,
                    "unit": "mm³"
                }
        
        # If we couldn't parse the output, return the error
        error_msg = result.get("output", "Unknown error")
        return {
            "status": "error",
            "error_message": f"Error calculating volume: {error_msg}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error calculating volume: {str(e)}"
        }

def calculate_surface_area(obj_name: str) -> dict:
    """Calculate the surface area of a FreeCAD object.
    
    Args:
        obj_name (str): Name of the object
    
    Returns:
        dict: A dictionary with the status and surface area information.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        # Calculate surface area
        result = client.run_python_code(f"""
import FreeCAD as App
doc = App.activeDocument()

# Check if object exists
obj = doc.getObject("{obj_name}")

if obj is None:
    print(f"Error: Object '{obj_name}' not found")
    result = {{"status": "error", "error_message": f"Object '{obj_name}' not found"}}
else:
    # Get the shape and calculate surface area
    try:
        # Check if object has a Shape
        if hasattr(obj, "Shape"):
            area = obj.Shape.Area
            print(f"Area calculation: {{'status': 'success', 'area': {area}, 'unit': 'mm²'}}")
            result = {{"status": "success", "area": {area}, "unit": "mm²"}}
        else:
            print(f"Error: Object '{obj_name}' has no Shape property")
            result = {{"status": "error", "error_message": f"Object '{obj_name}' has no Shape property"}}
    except Exception as e:
        print(f"Error calculating surface area: {{str(e)}}")
        result = {{"status": "error", "error_message": f"Error calculating surface area: {{str(e)}}"}}
""")
        
        # Check if the operation was successful
        if "success" in result.get("output", ""):
            # Extract area from output
            import re
            match = re.search(r"'area': (\d+\.?\d*)", result.get("output", ""))
            if match:
                area = float(match.group(1))
                return {
                    "status": "success",
                    "area": area,
                    "unit": "mm²"
                }
        
        # If we couldn't parse the output, return the error
        error_msg = result.get("output", "Unknown error")
        return {
            "status": "error",
            "error_message": f"Error calculating surface area: {error_msg}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error calculating surface area: {str(e)}"
        }

def calculate_center_of_mass(obj_name: str) -> dict:
    """Calculate the center of mass of a FreeCAD object.
    
    Args:
        obj_name (str): Name of the object
    
    Returns:
        dict: A dictionary with the status and center of mass information.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        # Calculate center of mass
        result = client.run_python_code(f"""
import FreeCAD as App
doc = App.activeDocument()

# Check if object exists
obj = doc.getObject("{obj_name}")

if obj is None:
    print(f"Error: Object '{obj_name}' not found")
    result = {{"status": "error", "error_message": f"Object '{obj_name}' not found"}}
else:
    # Get the shape and calculate center of mass
    try:
        # Check if object has a Shape
        if hasattr(obj, "Shape"):
            center = obj.Shape.CenterOfMass
            print(f"Center of mass: {{'status': 'success', 'x': {center.x}, 'y': {center.y}, 'z': {center.z}, 'unit': 'mm'}}")
            result = {{"status": "success", "x": {center.x}, "y": {center.y}, "z": {center.z}, "unit": "mm"}}
        else:
            print(f"Error: Object '{obj_name}' has no Shape property")
            result = {{"status": "error", "error_message": f"Object '{obj_name}' has no Shape property"}}
    except Exception as e:
        print(f"Error calculating center of mass: {{str(e)}}")
        result = {{"status": "error", "error_message": f"Error calculating center of mass: {{str(e)}}"}}
""")
        
        # Check if the operation was successful
        if "success" in result.get("output", ""):
            # Extract coordinates from output
            import re
            match = re.search(r"'x': ([-\d.]+), 'y': ([-\d.]+), 'z': ([-\d.]+)", result.get("output", ""))
            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                z = float(match.group(3))
                return {
                    "status": "success",
                    "center_of_mass": {
                        "x": x,
                        "y": y,
                        "z": z
                    },
                    "unit": "mm"
                }
        
        # If we couldn't parse the output, return the error
        error_msg = result.get("output", "Unknown error")
        return {
            "status": "error",
            "error_message": f"Error calculating center of mass: {error_msg}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error calculating center of mass: {str(e)}"
        }

def analyze_model_structure() -> dict:
    """Analyze the structure of the FreeCAD model to identify potential issues and provide recommendations.
    
    Returns:
        dict: A dictionary with the analysis results.
    """
    client = get_mcp_client()
    if client is None:
        return {
            "status": "error",
            "error_message": "Failed to connect to FreeCAD MCP server."
        }
    
    try:
        # Analyze the model
        result = client.run_python_code("""
import FreeCAD as App
import json

# Helper function to get object type in a user-friendly format
def get_object_type(obj):
    if hasattr(obj, "TypeId"):
        return obj.TypeId
    else:
        return str(type(obj))

# Check if any document exists
doc = App.activeDocument()
if doc is None:
    print(json.dumps({"status": "error", "error_message": "No active document found"}))
else:
    # Analyze model
    object_count = len(doc.Objects)
    
    # Get object types and counts
    object_types = {}
    for obj in doc.Objects:
        obj_type = get_object_type(obj)
        if obj_type in object_types:
            object_types[obj_type] += 1
        else:
            object_types[obj_type] = 1
    
    # Look for potential issues
    issues = []
    if object_count > 100:
        issues.append("Large number of objects may cause performance issues")
    
    # Check for objects with zero volume
    zero_volume_objects = []
    for obj in doc.Objects:
        if hasattr(obj, "Shape") and hasattr(obj.Shape, "Volume"):
            if obj.Shape.Volume < 0.0001:  # Almost zero
                zero_volume_objects.append(obj.Name)
    
    if zero_volume_objects:
        issues.append(f"Objects with zero or very small volume: {', '.join(zero_volume_objects)}")
    
    # Check for overlapping objects
    # This is simplified and would need more complex analysis for a real check
    
    # Create analysis result
    analysis = {
        "status": "success",
        "object_count": object_count,
        "object_types": object_types,
        "potential_issues": issues,
        "recommendations": []
    }
    
    # Add recommendations based on issues
    if "Large number of objects" in str(issues):
        analysis["recommendations"].append("Consider simplifying the model by combining objects or using patterns")
    
    if zero_volume_objects:
        analysis["recommendations"].append("Review and fix zero-volume objects as they may cause issues in manufacturing or analysis")
    
    print(json.dumps(analysis))
""")
        
        # Parse the output to get the analysis result
        if result and hasattr(result, "get"):
            output = result.get("output", "{}")
            try:
                # Try to parse the JSON output
                import json
                analysis = json.loads(output)
                return analysis
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "error_message": f"Failed to parse analysis result: {output}"
                }
        else:
            return {
                "status": "error",
                "error_message": "Failed to run analysis script"
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error analyzing model structure: {str(e)}"
        } 