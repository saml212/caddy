# CAD Agent System

This repository hosts a system of AI agents designed to help engineers with CAD modeling tasks, built using Google's Agent Development Kit (ADK).

## Overview

The CAD Agent System leverages the FreeCAD MCP (Mission Control Protocol) as a submodule to provide an intelligent assistant framework for CAD design tasks. The system uses Google's ADK to create specialized agents that can understand and assist with various aspects of CAD modeling.

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

## Quick Installation

```bash
# Install uv if you don't have it
curl -sSf https://install.pypa.io/rs/uv | python -

# Clone the repository
git clone https://github.com/saml212/caddy.git
cd caddy

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Configure your environment
cp .env.example .env
# Edit .env with your credentials
```

For more detailed instructions, see [INSTALL.md](INSTALL.md).

## Usage

After installation and configuration:

```bash
# Start the web interface
adk web

# Or use the command line interface
adk run cad_agents.main
```

## Prerequisites

- Python 3.9 or higher
- FreeCAD with MCP server enabled
- Google Cloud account (for Vertex AI) or Google AI API key

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License 