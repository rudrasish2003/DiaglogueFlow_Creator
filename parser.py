import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def parse_job_description(job_description, industry="general"):
    """
    Parse job description text into structured data using Gemini
    """
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
        # Find JSON content in response (handles cases where text has additional content)
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
    """
    Enhance the parsed data with industry-specific details
    """
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