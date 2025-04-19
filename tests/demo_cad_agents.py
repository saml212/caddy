#!/usr/bin/env python3
"""Demonstration script for the CAD Agents system.

This script shows how to use the CAD Agents to create a complex model
by interacting with the agents programmatically.
"""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(project_root)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import CAD Agents modules
from cad_agents.agents.root_agent import root_agent
from cad_agents.utils.mcp_utils import get_mcp_tools_async

async def check_mcp_connection_async():
    """Check MCP connection using the async ADK MCPToolset method."""
    logger.info("Checking MCP connection using ADK MCPToolset...")
    tools, exit_stack = await get_mcp_tools_async()
    if tools and exit_stack:
        logger.info(f"Successfully connected to FreeCAD MCP server. Found {len(tools)} tools.")
        await exit_stack.aclose() # Ensure connection is closed
        return True
    else:
        logger.warning("Could not connect to FreeCAD MCP server via ADK MCPToolset.")
        return False

async def run_demo():
    """Run the CAD Agents demonstration."""
    # Load environment variables
    load_dotenv()
    
    # Check MCP connection using the async method
    if not await check_mcp_connection_async():
        logger.error("Failed to connect to FreeCAD MCP server. Make sure FreeCAD is running with the MCP server enabled.")
        return False
    
    # Initialize the Google ADK runtime
    try:
        from google.adk.runtime import Runtime
        from google.adk.type.conversations import Message
        from google.adk.tools.tool_protos import FunctionCall, FunctionResponse
        
        # Create a runtime with the root agent
        runtime = Runtime(agent=root_agent)
        
        # Create a new conversation session
        session = runtime.start_session()

        # Step 0: Ensure a new document is created and active
        logger.info("Step 0: Creating a new FreeCAD document...")
        # Use execute_code tool directly via agent to create a document
        response = await session.send_message(
            Message.user("Create a new document named 'RocketDemo'")
        )
        # Check response for success/failure if possible, or just proceed
        for event in response.events:
             if event.content and event.content.parts:
                 print(f"Agent: {event.content.parts[0].text}")
             # Look for tool result if needed
             if isinstance(event, FunctionResponse) and event.name == 'execute_code':
                 if 'error' in event.response:
                     logger.error(f"Failed to create document via execute_code: {event.response['error']}")
                     return False
                 else:
                     logger.info("Document creation command sent.")

        # Add a small delay to allow FreeCAD GUI to potentially update
        await asyncio.sleep(1) 

        # Step 1: Create a basic model
        logger.info("Step 1: Creating a basic model...")
        response = await session.send_message(
            Message.user("Using the current document 'RocketDemo', I want to create a simple rocket model. "
                         "Start with a cylinder for the body, a cone for the nose, and some fins at the bottom.")
        )
        for event in response.events:
            if event.content and event.content.parts:
                print(f"Agent: {event.content.parts[0].text}")
        
        # Step 2: Modify the model dimensions
        logger.info("Step 2: Modifying the model dimensions...")
        response = await session.send_message(
            Message.user("Make the rocket body 50mm tall with a radius of 10mm. "
                         "The nose cone should be 20mm tall. Add three triangular fins.")
        )
        for event in response.events:
            if event.content and event.content.parts:
                print(f"Agent: {event.content.parts[0].text}")
        
        # Step 3: Analyze the model
        logger.info("Step 3: Analyzing the model...")
        response = await session.send_message(
            Message.user("Can you analyze this rocket model and tell me its volume and center of mass?")
        )
        for event in response.events:
            if event.content and event.content.parts:
                print(f"Agent: {event.content.parts[0].text}")
        
        # Step 4: Make improvements based on analysis
        logger.info("Step 4: Improving the model...")
        response = await session.send_message(
            Message.user("Suggest some improvements to this rocket design for better stability.")
        )
        for event in response.events:
            if event.content and event.content.parts:
                print(f"Agent: {event.content.parts[0].text}")
        
        # Step 5: Save the model
        logger.info("Step 5: Saving the model...")
        response = await session.send_message(
            Message.user("Save this rocket model as 'rocket_design.FCStd'.")
        )
        for event in response.events:
            if event.content and event.content.parts:
                print(f"Agent: {event.content.parts[0].text}")
        
        logger.info("Demo completed successfully!")
        return True
    
    except Exception as e:
        logger.error(f"Error running demo: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(run_demo())
        if not result:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1) 