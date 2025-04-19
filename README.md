# CAD Agent System

This repository hosts a system of AI agents designed to help engineers with CAD modeling tasks, built using Google's Agent Development Kit (ADK).

## Overview

The CAD Agent System leverages the FreeCAD MCP (Mission Control Protocol) as a submodule to provide an intelligent assistant framework for CAD design tasks. The system uses Google's ADK to create specialized agents that can understand and assist with various aspects of CAD modeling.

## Quick Start Guide

For a quick check if your system meets the requirements:

```bash
python3 check_prerequisites.py
```

### 1. Prerequisites
- Python 3.10 or higher (required for MCP tools)
- FreeCAD with MCP server enabled
- Google Cloud account or Google AI API key

### 2. Installation

```bash
# Clone the repository with its submodule
git clone https://github.com/saml212/caddy.git
cd caddy
git submodule update --init --recursive

# Install uv if you don't have it
curl -sSf https://install.pypa.io/rs/uv | python3 -

# Set up environment (requires Python 3.10+)
uv venv --python=python3.10
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### 3. Configure

```bash
# Set up your environment variables
cp .env.example .env
# Edit .env with your API credentials
```

### 4. Start FreeCAD with MCP

Launch FreeCAD and make sure the MCP server is running:
- Open FreeCAD
- Go to Edit > Preferences > General > Mission Control
- Enable the MCP server
- Click Apply and restart FreeCAD

### 5. Run the Agents

```bash
# Run the web interface
adk web

# Or use the command line interface
adk run cad_agents.main
```

For more detailed instructions, see [INSTALL.md](INSTALL.md).

## Features

- Agent-assisted CAD modeling with enhanced capabilities
- Intelligent design suggestions
- Automated routine tasks
- Knowledge-based design support
- Multi-agent architecture (design and analysis agents)

## Agent Capabilities

### Design Agent
The Design Agent can help you create and modify CAD models with these capabilities:
- Create primitive shapes (boxes, cylinders, spheres)
- Perform boolean operations (fusion, cut, common)
- Position and rotate objects in 3D space
- List existing objects in the model
- Save the current model

### Analysis Agent
The Analysis Agent can provide insights about your CAD models:
- Calculate object properties (volume, surface area, center of mass)
- Analyze model structure and identify potential issues
- Provide suggestions for model optimization
- Review design for manufacturability

## Architecture

The system consists of multiple specialized agents that work together to provide a comprehensive CAD assistance experience:

1. **Root Agent**: Coordinates between specialized agents based on user intent
2. **Design Agent**: Creates and modifies CAD models
3. **Analysis Agent**: Evaluates and analyzes CAD models

This multi-agent architecture leverages Google ADK's delegation capabilities to route user queries to the appropriate agent based on their intent.

## System Components

The CAD Agent system integrates these key components:
1. **FreeCAD**: The open-source CAD application that handles the actual modeling
2. **FreeCAD RPC Server (port 9876)**: Provides direct control of FreeCAD via XML-RPC
3. **MCP Server (port 5050)**: Translates between the RPC server and the MCP protocol
4. **Google ADK**: The framework that powers the intelligent agents

## Prerequisites

- Python 3.10 or higher (required for MCP tools)
- FreeCAD with MCP server enabled
- Google Cloud account (for Vertex AI) or Google AI API key

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License 