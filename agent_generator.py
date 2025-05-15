import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def load_industry_template(industry):
    """
    Load industry-specific template or fall back to general
    """
    try:
        template_path = f"templates/{industry.lower()}.json"
        if not os.path.exists(template_path):
            template_path = "templates/general.json"
            
        with open(template_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading template: {e}")
        # Return minimal template
        return {
            "entities": [],
            "standard_recruitment_flow": {},
            "industry_specific_parameters": {}
        }

def generate_standardized_recruitment_flow(parsed_info, industry):
    """
    Generate a recruitment agent using the standardized flow from the template
    with LLM fallback for handling questions outside the standard flow
    """
    # Load the appropriate industry template
    template = load_industry_template(industry)
    
    # Extract standardized flow from template
    flow = template.get("standard_recruitment_flow", {})
    industry_params = template.get("industry_specific_parameters", {})
    
    # Get company-specific info from parsed data
    company_name = parsed_info.get("company_name", "the company")
    position_title = parsed_info.get("position_title", "the position")
    
    # Create a formatted job description for the LLM context
    job_description_context = f"""
    Position: {position_title}
    Company: {company_name}
    Requirements: {parsed_info.get('required_qualifications', '')}
    Pay: {parsed_info.get('pay_rate', '')}
    Schedule: {parsed_info.get('schedule_type', '')}
    Benefits: {parsed_info.get('benefits', '')}
    Location: {parsed_info.get('location', '')}
    """
    
    prompt = f"""
    Create a detailed Dialogflow CX specification for a {industry} recruitment agent for {company_name}.
    
    Position: {position_title}
    Company: {company_name}
    
    Use this EXACT conversation flow structure:
    {json.dumps(flow, indent=2)}
    
    And these industry-specific parameters:
    {json.dumps(industry_params, indent=2)}
    
    The full job details are:
    {json.dumps(parsed_info, indent=2)}
    
    IMPORTANT: Include a special "Candidate Questions Handling" section with:
    
    1. A robust fallback intent to catch any candidate questions not in the standard flow
    2. Configuration for a webhook that will call an LLM to answer these questions
    3. A way to track the conversation state so the agent can resume the standard flow after answering questions
    
    The LLM should use this job information as context:
    {job_description_context}
    
    Generate a complete specification document with:
    1. All conversation pages following the exact flow provided
    2. Appropriate parameters for each page
    3. Entity definitions
    4. Routing logic between pages
    5. Fulfillment messages that sound natural and conversational
    6. The LLM fallback handling for out-of-context questions
    
    Format this as a comprehensive Dialogflow CX specification document.
    """
    
    try:
        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Return the markdown text directly
        return response.text
        
    except Exception as e:
        print(f"Error generating standardized recruitment flow: {e}")
        raise

def generate_webhook_code(parsed_info):
    """
    Generate the webhook code for LLM integration with Dialogflow CX
    """
    prompt = f"""
    Create a Node.js webhook function for Dialogflow CX that:
    
    1. Processes candidate questions that fall outside the standard recruitment flow
    2. Uses Google's Generative AI (Gemini) to generate relevant answers based on the job description
    3. Returns the answer to Dialogflow CX in the correct format
    4. Maintains conversation context to continue the standard flow afterward
    
    The job details to use as context are:
    {json.dumps(parsed_info, indent=2)}
    
    Include:
    - Complete code with proper error handling
    - Instructions for deployment to Cloud Functions
    - How to configure the webhook in Dialogflow CX
    
    Return the code with detailed comments.
    """
    
    try:
        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Return the webhook code
        return response.text
        
    except Exception as e:
        print(f"Error generating webhook code: {e}")
        raise