# Setting Up FreeCAD with the Google ADK Agent

This guide provides step-by-step instructions for setting up FreeCAD to work with the Google ADK agent system.

## Prerequisites

- Python 3.10 or higher
- FreeCAD 1.0.0 or higher
- Google API key or Google Cloud project

## Installation Steps

### 1. Install FreeCAD

Download and install FreeCAD from the [official website](https://www.freecad.org/downloads.php) or use package managers:

```bash
# macOS with Homebrew
brew install --cask freecad
```

### 2. Install the FreeCAD MCP Addon

The FreeCAD MCP (Mission Control Protocol) addon needs to be installed in FreeCAD:

```bash
# Clone the repository if you haven't already
git clone https://github.com/saml212/caddy.git
cd caddy
git submodule update --init --recursive

# Copy the MCP addon to FreeCAD's addon directory
# For macOS:
cp -r freecad-mcp/addon/FreeCADMCP ~/Library/Application\ Support/FreeCAD/Mod/

# For Windows:
# cp -r freecad-mcp/addon/FreeCADMCP %APPDATA%\FreeCAD\Mod\

# For Linux:
# cp -r freecad-mcp/addon/FreeCADMCP ~/.FreeCAD/Mod/
```

### 3. Configure FreeCAD for MCP

1. Launch FreeCAD
2. Go to Edit > Preferences > General > Mission Control
3. Enable the MCP server and set the port to 5050
4. Click Apply and restart FreeCAD

### 4. Start the RPC Server in FreeCAD

1. In FreeCAD, select the "MCP Addon" workbench from the workbench selector dropdown
2. Click the "Start RPC Server" button in the MCP Addon toolbar
3. You should see a message in the FreeCAD console: "RPC Server started at localhost:9876"

### 5. Set Up the Google ADK Environment

1. Create a virtual environment:
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

2. Configure the `.env` file:
   ```bash
   cp .env.example .env
   # Edit the .env file with your API credentials
   ```

### 6. Verify the Setup

To verify that the setup is working correctly, run the test script:

```bash
source .venv/bin/activate
python test_freecad_connection.py
```

If everything is set up correctly, you should see:
```
✅ Successfully connected to FreeCAD RPC server on port 9876
✅ MCP server is running on port 5050
✅ All connections successful!
✅ Successfully connected to both FreeCAD RPC and MCP servers!
```

## Running the CAD Agents

Once everything is correctly set up, you can run the CAD agents:

```bash
# Run the web interface
adk web

# Or use the command line interface
adk run cad_agents.main
```

## Troubleshooting

### Connection Issues

If you encounter connection issues:

1. Make sure FreeCAD is running
2. Ensure the MCP server is enabled in FreeCAD's preferences
3. Check that the RPC server is started from the MCP Addon workbench
4. Verify that both ports (5050 for MCP and 9876 for RPC) are available and not blocked by firewalls

### Missing Tools

If the ADK agent can't find the FreeCAD tools:

1. Check that the FreeCADMCP addon is properly installed
2. Restart FreeCAD after enabling the MCP server
3. Ensure the RPC server is running

## Architecture

The CAD Agent system uses a multi-component architecture:

1. **FreeCAD**: The CAD application that handles the actual modeling
2. **FreeCAD RPC Server (port 9876)**: Started from the MCP Addon workbench, provides an XML-RPC interface to control FreeCAD
3. **FreeCAD MCP Server (port 5050)**: Enabled in FreeCAD preferences, translates between the RPC server and the MCP protocol
4. **Google ADK Agent**: Connects to the MCP server to provide AI assistance for CAD modeling

This architecture allows the AI agent to control FreeCAD while maintaining a clean separation of concerns. 