# FreeCAD-Google ADK Integration Guide

This document explains how the FreeCAD CAD Agent system integrates with Google's Agent Development Kit (ADK), providing a comprehensive understanding of the architecture, design patterns, and best practices used in this project.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [System Components](#system-components)
- [Multi-Agent Architecture](#multi-agent-architecture)
- [Tool Implementation](#tool-implementation)
- [ADK Integration Details](#adk-integration-details)
- [Best Practices](#best-practices)
- [Extending the System](#extending-the-system)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The FreeCAD-Google ADK Integration uses a dual-server architecture to connect the Google ADK with FreeCAD:

```
+----------------+      +----------------+      +----------------+      +----------------+
|                |      |                |      |                |      |                |
|  Google ADK    | ---> |  MCP Server    | ---> |  FreeCAD RPC   | ---> |  FreeCAD      |
|  Agent System  |      |  (port 5050)   |      |  (port 9876)   |      |  Application  |
|                |      |                |      |                |      |                |
+----------------+      +----------------+      +----------------+      +----------------+
```

This architecture allows the ADK-powered agents to control FreeCAD through a standardized protocol (MCP), which is translated into RPC calls that FreeCAD can understand.

## System Components

### 1. FreeCAD Application

FreeCAD is the open-source CAD system that handles the actual 3D modeling operations. It runs the MCP Addon, which enables external control.

### 2. FreeCAD RPC Server (port 9876)

- Started from the FreeCAD MCP Addon
- Provides an XML-RPC interface to control FreeCAD
- Handles primitive operations like creating/modifying objects, executing Python code, etc.
- Located in `freecad-mcp/addon/FreeCADMCP/rpc_server/rpc_server.py`

### 3. MCP Server (port 5050)

- Translates between the Google ADK Model Control Protocol and the FreeCAD RPC protocol
- Provides a standardized interface for agents to interact with FreeCAD
- Implements a set of high-level tools that the agents can use
- Located in `freecad-mcp/src/freecad_mcp/server.py`

### 4. Google ADK Agents

- A system of specialized AI agents that provide CAD assistance
- Root agent for coordinating between specialized agents
- Design agent for creating and modifying models
- Analysis agent for evaluating models
- Located in `cad_agents/agents/`

## Multi-Agent Architecture

The CAD Agent system uses ADK's multi-agent capabilities to create a hierarchical agent structure:

1. **Root Agent (`root_agent.py`)**: 
   - Serves as the entry point for user interactions
   - Uses ADK's delegation capabilities to route requests to appropriate specialized agents
   - Makes decisions based on user intent (design vs. analysis)

2. **Design Agent (`design_agent.py`)**:
   - Specialized in creating and modifying CAD models
   - Has access to design-specific tools (create shapes, boolean operations, etc.)
   - Understands design terminology and requirements

3. **Analysis Agent (`analysis_agent.py`)**:
   - Specialized in analyzing and evaluating CAD models
   - Has access to analysis-specific tools (calculate properties, analyze structure, etc.)
   - Can provide insights and recommendations based on analysis results

This architecture leverages Google ADK's `SequentialAgent` pattern for workflow orchestration and dynamic LLM-driven delegation for flexible routing based on user intent.

## Tool Implementation

The tools that enable the agents to interact with FreeCAD are structured in two layers:

1. **FreeCAD Tools (`freecad_tools.py`)**:
   - Basic design operations (create shapes, boolean operations, etc.)
   - Utility operations (list objects, save documents, etc.)
   - Each tool connects to FreeCAD via the MCP client

2. **Analysis Tools (`analysis_tools.py`)**:
   - Specialized operations for analyzing models
   - Property calculations (volume, surface area, center of mass)
   - Model structure analysis and recommendations

The tools use the MCP client to send commands to the MCP Server, which translates them into FreeCAD RPC calls.

## ADK Integration Details

### ADK-MCP Integration

The integration between Google ADK and the MCP server is implemented using ADK's Model Control Protocol (MCP) toolkit. This allows the ADK agents to connect to the MCP server and use its tools.

Key files:
- `cad_agents/utils/mcp_utils.py`: Utilities for connecting to the MCP server
- `test_adk_freecad.py`: Test script for verifying the ADK-MCP integration

### Agent Definition

The CAD agents are defined using ADK's `Agent` class from `google.adk.agents`. Each agent is configured with:

1. **Model**: Which LLM to use (e.g., "gemini-2.5-pro")
2. **Name**: A unique identifier for the agent
3. **Description**: What the agent does (used for delegation decisions)
4. **Instruction**: How the agent should behave and what it should do
5. **Tools**: The tools the agent can use

Example:
```python
design_agent = Agent(
    name="design_agent",
    model="gemini-2.5-pro",
    description="Agent responsible for creating and modifying CAD models.",
    instruction="...",
    tools=[...]
)
```

### Agent Coordination

The agents coordinate using ADK's multi-agent capabilities:
- The root agent has design_agent and analysis_agent as sub-agents
- The LLM decides which agent to use based on the user's request
- Transfer between agents happens seamlessly

## Best Practices

### 1. Tool Design

- **Consistent Return Structure**: All tools return a dictionary with a "status" key ("success" or "error")
- **Error Handling**: All tools catch exceptions and return meaningful error messages
- **Documentation**: All tools have clear docstrings explaining their purpose and parameters

### 2. Agent Design

- **Clear Separation of Concerns**: Each agent has a specific responsibility
- **Focused Instructions**: Each agent's instructions clearly define its role and capabilities
- **Descriptive Names**: Agent names and descriptions make their roles clear

### 3. MCP Integration

- **Connection Management**: The MCP client is reused to avoid connection overhead
- **Robust Error Handling**: All MCP interactions include error handling
- **Output Parsing**: Careful parsing of MCP server responses for reliable data extraction

## Extending the System

### Adding New Tools

1. Identify the operation you want to add (e.g., a new shape type)
2. Add a new function to `freecad_tools.py` or `analysis_tools.py`
3. Follow the existing pattern for error handling and return structure
4. Add the tool to the appropriate agent in `design_agent.py` or `analysis_agent.py`

### Adding New Agents

1. Create a new file in `cad_agents/agents/` (e.g., `fabrication_agent.py`)
2. Define the agent using the Agent class from ADK
3. Create specialized tools in a new file under `cad_agents/tools/`
4. Add the new agent to `root_agent.py` as a sub-agent

## Troubleshooting

### Connection Issues

If the agents can't connect to FreeCAD:

1. Ensure FreeCAD is running
2. Check that the MCP Addon is installed and activated
3. Verify that the MCP server is enabled in FreeCAD preferences
4. Confirm that the RPC server is started by clicking the button in the MCP Addon toolbar
5. Check that ports 5050 (MCP) and 9876 (RPC) are not blocked by firewalls

### Agent Issues

If the agents are not behaving as expected:

1. Check the agent instructions for clarity and completeness
2. Verify that the right tools are attached to each agent
3. Examine the log output for errors
4. Use the test scripts to verify basic functionality

## Further Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [FreeCAD API Documentation](https://wiki.freecad.org/FreeCAD_API)
- [MCP Protocol Specification](https://google.github.io/adk-docs/tools/mcp-tools/) 