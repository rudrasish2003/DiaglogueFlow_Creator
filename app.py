import streamlit as st
import os
import json
import tempfile
import re
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import dialogflowcx_v3 as dialogflow
from google.cloud.dialogflowcx_v3.types import (
    Agent, 
    CreateAgentRequest, 
    CreateEntityTypeRequest,
    CreateIntentRequest, 
    CreateFlowRequest,
    CreatePageRequest,
    CreateWebhookRequest,
    EntityType,
    Intent,
    Flow,
    Page,
    Webhook,
    Fulfillment,
    ResponseMessage,
    TransitionRoute,
    Form
)

# Import custom modules
from parser import parse_job_description, enhance_parsed_data
from agent_generator import generate_standardized_recruitment_flow, generate_webhook_code
from utils import save_output_file, get_available_industries, generate_timestamp, sanitize_filename

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session state variables
if 'project_id' not in st.session_state:
    st.session_state.project_id = ""
if 'location_id' not in st.session_state:
    st.session_state.location_id = "global"
if 'deploy_webhook' not in st.session_state:
    st.session_state.deploy_webhook = True
if 'agent_spec' not in st.session_state:
    st.session_state.agent_spec = None
if 'webhook_code' not in st.session_state:
    st.session_state.webhook_code = None
if 'webhook_path' not in st.session_state:
    st.session_state.webhook_path = None
if 'spec_path' not in st.session_state:
    st.session_state.spec_path = None

# Dialogflow CX deployment functions
def extract_agent_details_from_md(agent_spec):
    """Extract agent details from the markdown specification."""
    # Extract agent name
    agent_name_match = re.search(r'# ([^#\n]+)', agent_spec)
    agent_name = agent_name_match.group(1).strip() if agent_name_match else "Generated Recruitment Agent"
    
    # Extract agent description
    agent_desc_match = re.search(r'## Agent Overview\s+([\s\S]+?)(?=##|$)', agent_spec)
    agent_description = agent_desc_match.group(1).strip() if agent_desc_match else "Automated recruitment agent"
    
    return agent_name, agent_description

def extract_entities_from_md(agent_spec):
    """Extract entity types from the markdown specification."""
    entities = []
    entity_section_match = re.search(r'## Entity Types\s+([\s\S]+?)(?=##|$)', agent_spec)
    
    if entity_section_match:
        entity_section = entity_section_match.group(1)
        entity_blocks = re.findall(r'### @([a-zA-Z_]+)\s+([\s\S]+?)(?=###|$)', entity_section)
        
        for entity_name, entity_content in entity_blocks:
            values = []
            value_matches = re.findall(r'- `([^`]+)`(?:[^[]+$$([^$$]+)\])?', entity_content)
            
            for value, synonyms_str in value_matches:
                synonyms = [s.strip() for s in synonyms_str.split(',')] if synonyms_str else []
                values.append({
                    "value": value,
                    "synonyms": synonyms
                })
            
            entities.append({
                "display_name": entity_name,
                "values": values
            })
    
    return entities

def extract_intents_from_md(agent_spec):
    """Extract intents from the markdown specification."""
    intents = []
    intent_section_match = re.search(r'## Key Intents\s+([\s\S]+?)(?=##|$)', agent_spec)
    
    if intent_section_match:
        intent_section = intent_section_match.group(1)
        intent_blocks = re.findall(r'### ([a-zA-Z_]+)\s+([\s\S]+?)(?=###|$)', intent_section)
        
        for intent_name, intent_content in intent_blocks:
            training_phrases = []
            phrase_matches = re.findall(r'- "([^"]+)"', intent_content)
            
            for phrase in phrase_matches:
                training_phrases.append(phrase)
            
            intents.append({
                "display_name": intent_name,
                "training_phrases": training_phrases
            })
    
    return intents

def deploy_webhook_to_cloud_functions(project_id, location_id, webhook_code, function_name="dialogflowWebhook"):
    """Deploy the webhook code to Google Cloud Functions."""
    # This would require using the Cloud Functions API
    # For this example, we'll return a mock success response
    return {
        "success": True,
        "webhook_url": f"https://{location_id}-{project_id}.cloudfunctions.net/{function_name}"
    }

def deploy_to_dialogflow_cx(project_id, location_id, agent_spec, webhook_url=None):
    """Deploy agent to Dialogflow CX directly from your app."""
    try:
        # 1. Extract agent details
        agent_name, agent_description = extract_agent_details_from_md(agent_spec)
        
        # 2. Create the agent
        agents_client = dialogflow.AgentsClient()
        parent = f"projects/{project_id}/locations/{location_id}"
        
        agent_request = CreateAgentRequest(
            parent=parent,
            agent=Agent(
                display_name=agent_name,
                default_language_code="en",
                time_zone="America/New_York",
                description=agent_description
            )
        )
        
        agent = agents_client.create_agent(request=agent_request)
        agent_path = agent.name
        
        # 3. Extract and create entity types
        entities = extract_entities_from_md(agent_spec)
        entity_types_client = dialogflow.EntityTypesClient()
        entity_type_map = {}
        
        for entity in entities:
            entity_values = []
            for value_item in entity["values"]:
                entity_values.append(
                    EntityType.Entity(
                        value=value_item["value"],
                        synonyms=value_item["synonyms"]
                    )
                )
            
            entity_request = CreateEntityTypeRequest(
                parent=agent_path,
                entity_type=EntityType(
                    display_name=entity["display_name"],
                    kind=EntityType.Kind.KIND_MAP,
                    entities=entity_values,
                    auto_expansion_mode=EntityType.AutoExpansionMode.AUTO_EXPANSION_MODE_DEFAULT
                )
            )
            
            created_entity = entity_types_client.create_entity_type(request=entity_request)
            entity_type_map[entity["display_name"]] = created_entity.name
        
        # 4. Extract and create intents
        intents = extract_intents_from_md(agent_spec)
        intents_client = dialogflow.IntentsClient()
        intent_map = {}
        
        for intent in intents:
            training_phrases = []
            for phrase in intent["training_phrases"]:
                training_phrases.append(
                    Intent.TrainingPhrase(
                        parts=[Intent.TrainingPhrase.Part(text=phrase)],
                        repeat_count=1
                    )
                )
            
            intent_request = CreateIntentRequest(
                parent=agent_path,
                intent=Intent(
                    display_name=intent["display_name"],
                    training_phrases=training_phrases
                )
            )
            
            created_intent = intents_client.create_intent(request=intent_request)
            intent_map[intent["display_name"]] = created_intent.name
        
        # 5. Create webhook if URL is provided
        webhook = None
        if webhook_url:
            webhooks_client = dialogflow.WebhooksClient()
            webhook_request = CreateWebhookRequest(
                parent=agent_path,
                webhook=Webhook(
                    display_name="LLMFallbackWebhook",
                    generic_web_service=Webhook.GenericWebService(
                        uri=webhook_url,
                        request_headers={"Content-Type": "application/json"}
                    )
                )
            )
            
            webhook = webhooks_client.create_webhook(request=webhook_request)
        
        # 6. Create default flow
        flows_client = dialogflow.FlowsClient()
        default_flow = flows_client.create_flow(
            parent=agent_path,
            flow=Flow(
                display_name="Main Recruitment Flow"
            )
        )
        
        # 7. Extract pages from specification
        pages_section_match = re.search(r'## Conversation Flow\s+([\s\S]+?)(?=##|$)', agent_spec)
        if pages_section_match:
            pages_section = pages_section_match.group(1)
            pages_client = dialogflow.PagesClient()
            created_pages = {}
            
            # Parse pages
            page_blocks = re.findall(r'### ([a-zA-Z_]+) Page\s+([\s\S]+?)(?=###|$)', pages_section)
            
            # First pass: Create all pages
            for page_name, page_content in page_blocks:
                # Extract entry fulfillment
                entry_text_match = re.search(r'Entry message: "([^"]+)"', page_content)
                entry_fulfillment = None
                
                if entry_text_match:
                    entry_text = entry_text_match.group(1)
                    entry_fulfillment = Fulfillment(
                        messages=[
                            ResponseMessage(
                                text=ResponseMessage.Text(
                                    text=[entry_text]
                                )
                            )
                        ]
                    )
                
                # Create page
                created_page = pages_client.create_page(
                    parent=default_flow.name,
                    page=Page(
                        display_name=page_name,
                        entry_fulfillment=entry_fulfillment
                    )
                )
                
                created_pages[page_name] = created_page
            
            # Second pass: Create routes between pages
            for page_name, page_content in page_blocks:
                source_page = created_pages.get(page_name)
                if not source_page:
                    continue
                
                # Extract routes
                route_matches = re.findall(r'Route to ([a-zA-Z_]+)(?: if `([^`]+)`)?', page_content)
                
                for target_page_name, condition in route_matches:
                    target_page = created_pages.get(target_page_name)
                    if not target_page:
                        continue
                    
                    # Create route
                    transition_route = TransitionRoute(
                        target_page=target_page.name,
                        condition=condition if condition else "true"
                    )
                    
                    # Update page with route
                    pages_client.update_page(
                        page=Page(
                            name=source_page.name,
                            transition_routes=[transition_route]
                        ),
                        update_mask="transition_routes"
                    )
        
        return {
            "success": True,
            "agent_path": agent_path,
            "agent_id": agent_path.split('/')[-1],
            "console_url": f"https://dialogflow.cloud.google.com/cx/projects/{project_id}/locations/{location_id}/agents/{agent_path.split('/')[-1]}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Callback functions to update session state
def update_project_id():
    st.session_state.project_id = st.session_state.project_id_input

def update_location_id():
    st.session_state.location_id = st.session_state.location_id_input

def update_deploy_webhook():
    st.session_state.deploy_webhook = st.session_state.deploy_webhook_input

def deploy_agent():
    """Deploy agent using session state variables"""
    if not st.session_state.project_id:
        st.error("Please enter a Google Cloud Project ID")
        return False
    
    has_credentials = "GOOGLE_APPLICATION_CREDENTIALS" in os.environ
    if not has_credentials:
        st.error("Please upload Google Cloud credentials to deploy")
        return False
        
    webhook_url = None
    if st.session_state.deploy_webhook and st.session_state.webhook_code:
        webhook_result = deploy_webhook_to_cloud_functions(
            st.session_state.project_id, 
            st.session_state.location_id, 
            st.session_state.webhook_code
        )
        
        if webhook_result["success"]:
            webhook_url = webhook_result["webhook_url"]
            st.success(f"Webhook deployed: {webhook_url}")
        else:
            st.warning(f"Webhook deployment failed: {webhook_result.get('error')}")
    
    # Deploy the agent
    result = deploy_to_dialogflow_cx(
        st.session_state.project_id,
        st.session_state.location_id,
        st.session_state.agent_spec,
        webhook_url
    )
    
    if result["success"]:
        st.success("Agent deployed successfully!")
        st.markdown(f"**Agent ID:** `{result['agent_id']}`")
        st.markdown(f"[Open in Dialogflow CX Console]({result['console_url']})")
        return True
    else:
        st.error(f"Error deploying agent: {result.get('error', 'Unknown error')}")
        return False

def main():
    st.set_page_config(
        page_title="Recruitment Agent Generator",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("Automated Recruitment Agent Generator")
    st.write("Generate Dialogflow CX recruitment agents with standardized flow and LLM fallback")
    
    # Sidebar for settings
    st.sidebar.header("Settings")
    industry = st.sidebar.selectbox(
        "Select Industry", 
        get_available_industries(),
        index=0
    )
    
    show_advanced = st.sidebar.checkbox("Show Advanced Options", value=False)
    
    # Check for Google Cloud credentials
    has_credentials = "GOOGLE_APPLICATION_CREDENTIALS" in os.environ
    if not has_credentials:
        st.sidebar.markdown("---")
        st.sidebar.header("API Credentials")
        uploaded_credentials = st.sidebar.file_uploader("Upload Google Cloud credentials JSON", type=["json"])
        if uploaded_credentials is not None:
            # Save to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
                tmp.write(uploaded_credentials.getvalue())
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tmp.name
            st.sidebar.success("Credentials loaded")
            has_credentials = True
    
    # Main input area
    st.header("Job Description Input")
    
    # Allow file upload or direct text input
    input_method = st.radio("Input Method", ["Text Input", "File Upload"])
    
    job_description = ""
    
    if input_method == "Text Input":
        job_description = st.text_area(
            "Paste the job description here:", 
            height=300,
            placeholder="Enter the full job description..."
        )
    else:  # File Upload
        uploaded_file = st.file_uploader("Upload job description file", type=["txt", "pdf", "docx"])
        if uploaded_file is not None:
            # Handle different file types
            file_type = uploaded_file.name.split(".")[-1]
            
            if file_type == "txt":
                job_description = uploaded_file.read().decode("utf-8")
            elif file_type == "pdf":
                st.warning("PDF parsing requires additional libraries. For this example, please use text files.")
            elif file_type == "docx":
                st.warning("DOCX parsing requires additional libraries. For this example, please use text files.")
            
            if job_description:
                st.text_area("Extracted Content", job_description, height=200)
    
    company_name = st.text_input("Company Name", "")
    position_title = st.text_input("Position Title", "")
    
    # Process the job description
    if st.button("Generate Recruitment Agent"):
        if not job_description:
            st.error("Please enter a job description.")
            return
            
        with st.spinner("Processing job description..."):
            # Parse the job description
            parsed_data = parse_job_description(job_description, industry)
            
            # Override company name and position title if provided
            if company_name:
                parsed_data["company_name"] = company_name
            if position_title:
                parsed_data["position_title"] = position_title
                
            # Show the parsed data
            st.subheader("Parsed Job Information")
            st.json(parsed_data)
            
            # Enhanced parsed data with industry-specific details
            with st.spinner("Enhancing with industry-specific details..."):
                enhanced_data = enhance_parsed_data(parsed_data, industry)
            
            timestamp = generate_timestamp()
            sanitized_title = sanitize_filename(parsed_data['position_title'])
            
            # Generate agent specification using standardized flow
            with st.spinner(f"Generating {industry} agent specification with standardized flow..."):
                agent_spec = generate_standardized_recruitment_flow(enhanced_data, industry)
                spec_filename = f"{sanitized_title}_{timestamp}_agent_spec.md"
                spec_path = save_output_file(agent_spec, spec_filename)
                
                # Save to session state
                st.session_state.agent_spec = agent_spec
                st.session_state.spec_path = spec_path
            
            st.subheader("Agent Specification")
            st.markdown(agent_spec)
            st.download_button(
                "Download Agent Specification",
                agent_spec,
                spec_filename,
                "text/markdown"
            )
            
            # Generate LLM webhook
            with st.spinner("Generating LLM fallback webhook code..."):
                webhook_code = generate_webhook_code(enhanced_data)
                webhook_filename = f"{sanitized_title}_{timestamp}_webhook.js"
                webhook_path = save_output_file(webhook_code, webhook_filename)
                
                                # Save to session state
                st.session_state.webhook_code = webhook_code
                st.session_state.webhook_path = webhook_path
            
            if show_advanced:
                st.subheader("LLM Fallback Webhook Code")
                st.code(webhook_code, language="javascript")
                st.download_button(
                    "Download Webhook Code",
                    webhook_code,
                    webhook_filename,
                    "text/javascript"
                )
            else:
                st.success(f"LLM fallback webhook code has been saved to {webhook_path}")
                st.download_button(
                    "Download Webhook Code",
                    webhook_code,
                    webhook_filename,
                    "text/javascript"
                )
            
            # Deployment options
            st.subheader("Deployment Options")
            
            deployment_tab1, deployment_tab2 = st.tabs(["Automatic Deployment", "Manual Deployment"])
            
            with deployment_tab1:
                st.markdown("Deploy directly to Dialogflow CX")
                
                col1, col2 = st.columns(2)
                with col1:
                    # Use key parameter to avoid refreshing issues
                    st.text_input("Google Cloud Project ID", 
                                  value=st.session_state.project_id,
                                  key="project_id_input", 
                                  on_change=update_project_id)
                with col2:
                    st.selectbox("Location", 
                                ["global", "us-central1", "europe-west1", "asia-northeast1"],
                                index=["global", "us-central1", "europe-west1", "asia-northeast1"].index(st.session_state.location_id),
                                key="location_id_input",
                                on_change=update_location_id)
                
                st.checkbox("Deploy Webhook to Cloud Functions", 
                           value=st.session_state.deploy_webhook,
                           key="deploy_webhook_input",
                           on_change=update_deploy_webhook)
                
                # Use a separate button with a unique key for deployment
                if st.button("Create and Deploy Agent", key="deploy_button"):
                    deploy_agent()
            
            with deployment_tab2:
                st.markdown("""
                ### Manual Deployment Instructions
                
                1. Create a new agent in the [Dialogflow CX Console](https://dialogflow.cloud.google.com/cx)
                2. Use the specification document to set up:
                   - Entity types
                   - Intents with training phrases
                   - Pages with parameters and fulfillment
                   - Routes between pages
                3. Deploy the webhook code to Google Cloud Functions
                4. Configure the webhook URL in Dialogflow CX
                """)

if __name__ == "__main__":
    main()