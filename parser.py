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
    2. "company_name": The company name (infer if not explicitly stated)
    3. "required_experience": Years or type of experience required
    4. "required_skills": List of required skills/certifications
    5. "required_qualifications": List of qualifications like licenses, certifications, etc.
    6. "pay_rate": Salary or hourly rate information
    7. "schedule_type": Working hours or shift information
    8. "location": Job location information
    9. "benefits": List of benefits offered
    10. "job_description": Brief summary of the job responsibilities
    11. "screening_requirements": List of screening requirements (background checks, drug tests, etc.)
    
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
            "company_name": "Unknown Company",
            "required_experience": "Not specified",
            "required_skills": [],
            "job_description": "No description available"
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
    1. "common_candidate_questions": List of 5-10 common questions candidates might ask about this role
    2. "question_answers": Dictionary of answers to common questions
    3. "objection_handling": Dictionary of common objections and how to address them
    4. "key_screening_questions": 5-8 key questions to ask candidates during screening
    5. "age_requirement": Minimum age requirement for the position (e.g., "21" for trucking)
    6. "qualification_checks": List of specific qualifications to verify (like "CDL", "DOT Medical Card", etc.)
    
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