# Installation Guide

This guide will help you set up and run the CAD Agents system.

## Prerequisites

- Python 3.9 or higher
- [FreeCAD](https://www.freecad.org/downloads.php) with MCP server enabled
- Google Cloud account (for Vertex AI) or Google AI API key

## Installation

### Using uv (Recommended)

1. Install [uv](https://github.com/astral-sh/uv) if you don't have it already:
   ```bash
   curl -sSf https://install.pypa.io/rs/uv | python -
   ```

2. Clone the repository and navigate to it:
   ```bash
   git clone https://github.com/saml212/caddy.git
   cd caddy
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

### Using pip

1. Clone the repository and navigate to it:
   ```bash
   git clone https://github.com/saml212/caddy.git
   cd caddy
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

## Configuration

1. Copy the sample environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your credentials:
   - If using Vertex AI:
     ```
     GOOGLE_GENAI_USE_VERTEXAI=True
     GOOGLE_CLOUD_PROJECT=your-project-id
     GOOGLE_CLOUD_LOCATION=us-central1
     ```
   - If using Google AI Studio:
     ```
     GOOGLE_GENAI_USE_VERTEXAI=False
     GOOGLE_API_KEY=your-api-key
     ```

## Setup FreeCAD MCP

1. Launch FreeCAD
2. Enable the MCP server:
   - Navigate to Edit > Preferences > General > Mission Control
   - Check "Enable Mission Control Server"
   - Set the port (default: 5050)
   - Click Apply and restart FreeCAD

## Running the CAD Agents

You can run the CAD Agents system using the ADK CLI:

```bash
# Run the web interface (recommended for local development)
adk web

# Or run the command line interface
adk run cad_agents.main
```

## Using Docker (Coming Soon) 