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
            "intents": [],
            "conversational_style": "professional and friendly"
        }

def generate_agent_builder_specification(parsed_info, industry):
    """
    Generate a document for Dialogflow CX Agent Builder
    """
    template = load_industry_template(industry)
    
    prompt = f"""
    Create a detailed Dialogflow CX Agent Builder specification document for a recruitment agent interviewing candidates for this position:
    
    {json.dumps(parsed_info, indent=2)}
    
    Industry context: {industry}
    Template guidelines: {json.dumps(template, indent=2)}
    
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
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        # Return the markdown text directly
        return response.text
        
    except Exception as e:
        print(f"Error generating agent specification: {e}")
        raise

def generate_dialogflow_cx_pages(parsed_info, industry):
    """
    Generate Dialogflow CX pages with conversational content
    """
    template = load_industry_template(industry)
    
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