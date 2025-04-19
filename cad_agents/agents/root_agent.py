"""Root Agent for coordinating CAD agent system."""

from google.adk.agents import Agent, SequentialAgent
from . import design_agent, analysis_agent

# Define a root agent that can delegate to specialized agents
root_agent = Agent(
    name="cad_assistant",
    model="gemini-2.0-pro",
    description="Main CAD assistant that understands user intent and delegates to specialized agents.",
    instruction="""
You are a CAD assistant that helps engineers design and analyze 3D models.
Your role is to understand the user's intent and delegate to the appropriate specialized agent:

1. The design_agent - for creating and modifying CAD models
2. The analysis_agent - for evaluating and analyzing CAD models

Look for keywords in the user's request to determine which agent to use:
- For design requests about creating, modifying, or building models, use the design_agent
- For analysis requests about evaluating, checking, or understanding models, use the analysis_agent

If the request is ambiguous, ask clarifying questions to determine the user's intent.
    """,
    tools=[
        design_agent.design_agent,  # Use the design agent as a tool
        analysis_agent.analysis_agent  # Use the analysis agent as a tool
    ]
)

# Create a sequential workflow that combines design and analysis
design_analyze_workflow = SequentialAgent(
    name="design_analyze_workflow",
    description="A workflow that first designs a model and then analyzes it.",
    agents=[
        design_agent.design_agent,
        analysis_agent.analysis_agent
    ]
) 