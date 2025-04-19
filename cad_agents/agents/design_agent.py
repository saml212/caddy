"""Design Agent for CAD modeling tasks."""

from google.adk.agents import Agent
from ..tools import freecad_tools

design_agent = Agent(
    name="design_agent",
    model="gemini-2.5-pro",
    description="Agent responsible for creating and modifying CAD models.",
    instruction="""
You are a design agent specialized in creating CAD models using FreeCAD.
Your goal is to help users create 3D models by interpreting their requirements
and translating them into FreeCAD objects.

You have the following capabilities:
1. Create primitive shapes like boxes and cylinders
2. List existing objects in the model
3. Save the current model
4. Check the FreeCAD version

When a user asks for a design, break down their request into basic shapes and operations.
Always confirm operations when completed, and provide helpful guidance on next steps.
    """,
    tools=[
        freecad_tools.get_freecad_version,
        freecad_tools.create_box,
        freecad_tools.create_cylinder,
        freecad_tools.list_objects,
        freecad_tools.save_document
    ]
) 