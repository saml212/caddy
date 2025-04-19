"""Analysis Agent for evaluating CAD models."""

from google.adk.agents import Agent
from ..tools import freecad_tools
from ..tools import analysis_tools

# We'll need to add specific analysis tools in the future,
# but for now we'll reuse the same tools from freecad_tools

analysis_agent = Agent(
    name="analysis_agent",
    model="gemini-2.5-pro",
    description="Agent responsible for analyzing CAD models.",
    instruction="""
You are an analysis agent specialized in evaluating CAD models created with FreeCAD.
Your goal is to help users understand the properties and characteristics of their 3D models.

You have the following capabilities:
1. List and examine objects in the model
2. Check the FreeCAD version
3. Calculate object properties (volume, surface area, center of mass)
4. Analyze the model structure and identify potential design issues
5. Provide suggestions for model optimization

When a user asks for analysis, focus on providing meaningful insights about the model structure.
Use your knowledge of engineering principles to suggest improvements or identify potential issues.
Always provide your reasoning along with any recommendations.
    """,
    tools=[
        freecad_tools.get_freecad_version,
        freecad_tools.list_objects,
        analysis_tools.calculate_volume,
        analysis_tools.calculate_surface_area,
        analysis_tools.calculate_center_of_mass,
        analysis_tools.analyze_model_structure
    ]
) 