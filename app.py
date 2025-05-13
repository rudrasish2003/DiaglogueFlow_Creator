import streamlit as st
import os
import json
import tempfile
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import dialogflowcx_v3 as dialogflow

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Helper functions
def get_available_industries():
    """Get list of available industry templates"""
    industries = ["general", "trucking", "healthcare", "technology", "retail"]
    return industries

def generate_timestamp():
    """Generate timestamp string for filenames"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def sanitize_filename(text):
    """Sanitize text for use in filenames"""
    return "".join([c if c.isalnum() else "_" for c in text]).strip("_")

def save_output_file(data, filename, output_dir="outputs"):
    """Save data to a file in the outputs directory"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'w') as file:
        if isinstance(data, str):
            file.write(data)
        else:
            json.dump(data, file, indent=2)
            
    return file_path

def parse_job_description(job_description, industry="general"):
    """Parse job description text into structured data using Gemini"""
    prompt = f"""
    Parse the following {industry} job description and extract key information for a recruitment conversation:
    
    {job_description}
    
    Format your response as a JSON object with these fields:
    1. "position_title": The job title
    2. "required_experience": Years or type of experience required
    3. "required_skills": List of required skills/certifications
    4. "pay_rate": Salary or hourly rate information
    5. "schedule_type": Working hours or shift information
    6. "key_questions": List of 5-7 specific questions to ask candidates
    7. "benefits": List of benefits offered
    8. "requirements": Any specific requirements like licenses, education, etc.
    
    JSON response only:
    """
    
    try:
        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Extract and parse JSON from response text
        response_text = response.text
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_content = response_text[json_start:json_end]
            parsed_data = json.loads(json_content)
            return parsed_data
        else:
            raise ValueError("No valid JSON found in response")
            
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        # Return a minimal valid structure
        return {
            "position_title": "Unknown Position",
            "required_experience": "Not specified",
            "required_skills": [],
            "key_questions": []
        }
    except Exception as e:
        print(f"Error parsing job description: {e}")
        raise

def enhance_parsed_data(parsed_data, industry):
    """Enhance the parsed data with industry-specific details"""
    prompt = f"""
    Enhance this parsed job data for a {industry} recruitment agent:
    
    {json.dumps(parsed_data, indent=2)}
    
    Add or improve:
    1. More detailed interview questions specific to this role
    2. Industry-specific terms to use in conversation
    3. Common candidate questions for this role with answers
    4. Objection handling for potential candidate concerns
    
    Return the complete enhanced JSON including all original fields plus new ones.
    JSON response only:
    """
    
    try:
        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Extract and parse JSON from response text
        response_text = response.text
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_content = response_text[json_start:json_end]
            enhanced_data = json.loads(json_content)
            return enhanced_data
        else:
            raise ValueError("No valid JSON found in response")
            
    except Exception as e:
        print(f"Error enhancing parsed data: {e}")
        return parsed_data  # Return original data if enhancement fails

def generate_agent_builder_specification(parsed_info, industry):
    """Generate a document for Dialogflow CX Agent Builder"""
    prompt = f"""
    Create a detailed Dialogflow CX Agent Builder specification document for a recruitment agent interviewing candidates for this position:
    
    {json.dumps(parsed_info, indent=2)}
    
    Industry context: {industry}
    
    Your response should be a comprehensive document formatted for direct upload to Dialogflow CX Agent Builder.
    Include these sections:
    
    # {parsed_info.get('position_title', 'Position')} Recruitment Agent
    
    ## Agent Overview
    [Describe the agent's purpose and conversation style]
    
    ## Conversation Flow
    [Detailed description of the full interview flow from greeting to conclusion]
    
    ## Questions To Ask Candidates
    [List all questions with explanations of why they're important]
    
    ## Candidate Question Handling
    [How to respond to common candidate questions about the position]
    
    ## Entity Types
    [List all entity types needed for parameter collection]
    
    ## Key Intents
    [List major intents with example training phrases]
    
    ## Conversational Elements
    [Examples of natural-sounding responses that show personality]
    """
    
    try:
        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Return the markdown text directly
        return response.text
        
    except Exception as e:
        print(f"Error generating agent specification: {e}")
        raise

def generate_dialogflow_cx_pages(parsed_info, industry):
    """Generate Dialogflow CX pages with conversational content"""
    prompt = f"""
    Create detailed Dialogflow CX pages for a recruitment agent interviewing candidates for this position:
    
    {json.dumps(parsed_info, indent=2)}
    
    Industry: {industry}
    
    Generate a JSON array of pages with these components for each page:
    
    1. "displayName": Page name
    2. "description": Brief description of the page's purpose
    3. "entryFulfillment": Response when entering the page, with 3 conversational variants
    4. "form": Parameter to collect (if any)
    5. "routes": Transitions to other pages
    
    Include these key pages:
    - Welcome (greeting and introduction)
    - Experience Questions (ask about candidate experience)
    - Skills Assessment (questions related to required skills)
    - Schedule Discussion (discuss work schedule preferences)
    - Candidate Questions (handle questions about job)
    - Scheduling (set up next steps)
    - Conclusion (end the conversation)
    
    Make all responses sound conversational, using casual language with filler words.
    JSON array of pages only.
    """
    
    try:
        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Extract and parse JSON from response text
        response_text = response.text
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_content = response_text[json_start:json_end]
            pages = json.loads(json_content)
            return pages
        else:
            raise ValueError("No valid JSON array found in response")
            
    except json.JSONDecodeError:
        print("Error: Response was not valid JSON")
        # Return minimal pages
        return [
            {
                "displayName": "Welcome",
                "entryFulfillment": {
                    "messages": [
                        {"text": {"text": ["Hello, this is the recruitment agent. How are you today?"]}}
                    ]
                }
            }
        ]
    except Exception as e:
        print(f"Error generating pages: {e}")
        raise

def deploy_to_dialogflow_cx(project_id, location, agent_name, agent_spec):
    """Create a new agent in Dialogflow CX using the API"""
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

def main():
    st.set_page_config(
        page_title="Recruitment Agent Generator",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("Automated Recruitment Agent Generator")
    st.write("Generate Dialogflow CX recruitment agents from job descriptions using Gemini")
    
    # Sidebar for settings
    st.sidebar.header("Settings")
    industry = st.sidebar.selectbox(
        "Select Industry", 
        get_available_industries(),
        index=0
    )
    
    show_advanced = st.sidebar.checkbox("Show Advanced Options", value=False)
    
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
    
    position_title = st.text_input("Position Title (Optional)", "")
    
    # Process the job description
    if st.button("Generate Recruitment Agent"):
        if not job_description:
            st.error("Please enter a job description.")
            return
            
        with st.spinner("Processing job description..."):
            # Parse the job description
            parsed_data = parse_job_description(job_description, industry)
            
            # Override position title if provided
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
            
            # Generate agent specification for Agent Builder
            with st.spinner("Generating agent specification..."):
                agent_spec = generate_agent_builder_specification(enhanced_data, industry)
                spec_filename = f"{sanitized_title}_{timestamp}_agent_spec.md"
                spec_path = save_output_file(agent_spec, spec_filename)
            
            st.subheader("Agent Builder Specification")
            st.markdown(agent_spec)
            st.download_button(
                "Download Agent Builder Specification",
                agent_spec,
                spec_filename,
                "text/markdown"
            )
            
            # Generate Dialogflow CX pages
            if show_advanced:
                with st.spinner("Generating Dialogflow CX pages..."):
                    dialogflow_pages = generate_dialogflow_cx_pages(enhanced_data, industry)
                    pages_filename = f"{sanitized_title}_{timestamp}_pages.json"
                    pages_path = save_output_file(dialogflow_pages, pages_filename)
                
                st.subheader("Dialogflow CX Pages")
                st.json(dialogflow_pages)
                st.download_button(
                    "Download Dialogflow CX Pages",
                    json.dumps(dialogflow_pages, indent=2),
                    pages_filename,
                    "application/json"
                )
            
            # Deployment options
            st.subheader("Deployment Options")
            st.markdown("""
            ### Option 1: Use Agent Builder (Recommended)
            1. Go to [Dialogflow CX Console](https://dialogflow.cloud.google.com/cx)
            2. Create a new agent
            3. Click on "Agent Settings" > "Agent Builder"
            4. Upload the specification markdown file
            
            ### Option 2: Manual Import
            1. Create a new agent in Dialogflow CX
            2. Add the entities and intents as specified
            3. Create the pages with the provided fulfillment messages
            """)
            
            if show_advanced:
                st.markdown("### Option 3: API Deployment (Advanced)")
                col1, col2 = st.columns(2)
                with col1:
                    project_id = st.text_input("Google Cloud Project ID")
                with col2:
                    location = st.selectbox("Location", ["global", "us-central1", "europe-west1", "asia-northeast1"])
                
                if st.button("Create Agent via API"):
                    if not project_id:
                        st.error("Please enter a Google Cloud Project ID")
                    else:
                        with st.spinner("Creating agent..."):
                            agent_name = f"{parsed_data['position_title']} Recruitment Agent"
                            result = deploy_to_dialogflow_cx(
                                project_id, 
                                location, 
                                agent_name,
                                agent_spec
                            )
                            
                            if result["success"]:
                                st.success(result["message"])
                                st.code(result["agent_path"])
                            else:
                                st.error(f"Error creating agent: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()