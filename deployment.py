import os
import json
import tempfile
from google.cloud import dialogflowcx_v3 as dialogflow
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def prepare_agent_builder_file(agent_spec):
    """
    Format the agent specification document for Agent Builder
    """
    # Agent Builder accepts markdown, so just return the doc
    return agent_spec

def deploy_to_dialogflow_cx(project_id, location, agent_name, agent_spec):
    """
    Create a new agent in Dialogflow CX using the API
    Note: This is a simplified version - full implementation would require
    converting the specification to API calls
    """
    try:
        # Create the agent
        agents_client = dialogflow.AgentsClient()
        parent = f"projects/{project_id}/locations/{location}"
        
        agent = {
            "display_name": agent_name,
            "default_language_code": "en",
            "time_zone": "America/New_York",
            "description": "Created by Automated Agent Generator"
        }
        
        created_agent = agents_client.create_agent(
            parent=parent,
            agent=agent
        )
        
        agent_path = created_agent.name
        
        return {
            "success": True,
            "agent_path": agent_path,
            "message": f"Agent created successfully. Use Agent Builder to import the specification document."
        }
            
    except Exception as e:
        print(f"Error creating agent: {e}")
        return {
            "success": False,
            "error": str(e)
        }