"""Main execution script for the CAD agent using MCP tools."""

import asyncio
import logging
import sys
from dotenv import load_dotenv

from google.genai import types as genai_types
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService # Optional, but good practice

from cad_agents.utils.mcp_utils import load_mcp_tools, close_mcp_connection

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file (if needed, e.g., for API keys)
load_dotenv()

async def get_agent_and_stack():
    """Creates an ADK Agent equipped with tools from the FreeCAD MCP Server."""
    logger.info("Loading tools from FreeCAD MCP Server...")
    tools, exit_stack = await load_mcp_tools()

    if tools is None or exit_stack is None:
        logger.error("Failed to load tools from MCP server. Agent cannot be created.")
        return None, None

    logger.info(f"Fetched {len(tools)} tools from MCP server.")
    
    # Define the agent that will use the MCP tools
    # Using the last model specified by the user
    agent = LlmAgent(
        model='gemini-2.5-flash-preview-04-17', 
        name='cad_assistant_mcp',
        instruction='You are a helpful CAD assistant interacting with FreeCAD. Use the available tools to fulfill the user\'s requests for creating, modifying, or analyzing CAD models.',
        tools=tools, # Provide the MCP tools directly to the ADK agent
    )
    
    logger.info(f"Agent '{agent.name}' created successfully.")
    return agent, exit_stack

async def async_main():
    """Main async function to run the interactive agent session."""
    agent, exit_stack = await get_agent_and_stack()

    if agent is None or exit_stack is None:
        logger.error("Exiting due to agent creation failure.")
        return

    # Ensure the MCP connection is closed when done
    async with exit_stack:
        session_service = InMemorySessionService()
        artifacts_service = InMemoryArtifactService() # Optional

        session = session_service.create_session(
            state={}, app_name='cad_agent_mcp_app', user_id='user_cli'
        )
        
        runner = Runner(
            app_name='cad_agent_mcp_app',
            agent=agent,
            artifact_service=artifacts_service, # Optional
            session_service=session_service,
        )

        logger.info(f"Running agent '{agent.name}', type 'exit' or Ctrl+C to quit.")

        while True:
            try:
                user_input = await asyncio.to_thread(input, "user: ")
                if user_input.lower() == 'exit':
                    logger.info("Exit command received.")
                    break
                
                content = genai_types.Content(role='user', parts=[genai_types.Part(text=user_input)])
                
                logger.info("Running agent...")
                events_async = runner.run_async(
                    session_id=session.id, user_id=session.user_id, new_message=content
                )
                
                final_response = ""
                async for event in events_async:
                    logger.debug(f"Event received: {event}")
                    if event.content and event.content.parts:
                         # Check for text parts specifically for printing
                         text_parts = [part.text for part in event.content.parts if hasattr(part, 'text') and part.text]
                         if text_parts:
                             response_chunk = "".join(text_parts)
                             print(f"[{event.author}]: {response_chunk}")
                             if event.type == 'FINAL_RESPONSE': # Accumulate final response
                                 final_response += response_chunk
                
                # If no text was printed in the final response event, indicate completion
                # if final_response:
                #     print(f"[{agent.name}]: {final_response}") # Print accumulated final response if needed

            except (KeyboardInterrupt, EOFError):
                logger.info("Interruption detected.")
                break
            except Exception as e:
                logger.error(f"An error occurred during the run loop: {e}", exc_info=True)
                # Decide whether to break or continue on error
                break 

    logger.info("Agent session finished.")


if __name__ == '__main__':
    try:
        asyncio.run(async_main())
    except ImportError:
         # Specific handling for the SseServerParams import error during testing
        logger.error("ImportError occurred. Could not import SseServerParams from google.adk.tools.mcp_tool.mcp_toolset.")
        logger.error("Please ensure 'google-adk' is installed correctly and the class exists.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Script finished.") 