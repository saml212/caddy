"""Analysis Agent for evaluating CAD models."""

from google.adk.agents import Agent
from ..tools import freecad_tools

# We'll need to add specific analysis tools in the future,
# but for now we'll reuse the same tools from freecad_tools

analysis_agent = Agent(
    name="analysis_agent",
    model="gemini-2.0-pro",
    description="Agent responsible for analyzing CAD models.",
    instruction="""
You are an analysis agent specialized in evaluating CAD models created with FreeCAD.
Your goal is to help users understand the properties and characteristics of their 3D models.

You have the following capabilities:
1. List existing objects in the model
2. Check the FreeCAD version

When a user asks for analysis, focus on providing meaningful insights about the model structure.
Use your knowledge of engineering principles to suggest improvements or identify potential issues.
Always provide your reasoning along with any recommendations.
    """,
    tools=[
        freecad_tools.get_freecad_version,
        freecad_tools.list_objects
    ]
) 