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

- Agent-assisted CAD modeling
- Intelligent design suggestions
- Automated routine tasks
- Knowledge-based design support
- Multi-agent architecture (design and analysis agents)

## Architecture

The system consists of multiple specialized agents that work together to provide a comprehensive CAD assistance experience:

1. **Root Agent**: Coordinates between specialized agents based on user intent
2. **Design Agent**: Creates and modifies CAD models
3. **Analysis Agent**: Evaluates and analyzes CAD models

## Prerequisites

- Python 3.10 or higher (required for MCP tools)
- FreeCAD with MCP server enabled
- Google Cloud account (for Vertex AI) or Google AI API key

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License 