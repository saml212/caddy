"""Root Agent for coordinating CAD agent system."""

from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool  # Import AgentTool
from . import design_agent, analysis_agent

# Define a root agent that can delegate to specialized agents
root_agent = Agent(
    name="cad_assistant",
    model="gemini-2.5-pro",
    description="Main CAD assistant that understands user intent and delegates to specialized agents.",
    instruction="""
You are a CAD assistant that helps engineers design and analyze 3D models.
Your role is to understand the user's intent and delegate to the appropriate specialized agent:

1. The design_agent - for creating and modifying CAD models
2. The analysis_agent - for evaluating and analyzing CAD models

Look for keywords in the user's request to determine which agent to use:
- For design requests about creating, modifying, or building models, use the design_agent tool.
- For analysis requests about evaluating, checking, or understanding models, use the analysis_agent tool.

If the request is ambiguous, ask clarifying questions to determine the user's intent.
    """,
    tools=[
        AgentTool(agent=design_agent.design_agent),  # Wrap design_agent in AgentTool
        AgentTool(agent=analysis_agent.analysis_agent)  # Wrap analysis_agent in AgentTool
    ]
)

# Create a sequential workflow that combines design and analysis
design_analyze_workflow = SequentialAgent(
    name="design_analyze_workflow",
    description="A workflow that first designs a model and then analyzes it.",
    sub_agents=[
        design_agent.design_agent,
        analysis_agent.analysis_agent
    ]
) 