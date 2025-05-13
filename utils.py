import os
import json
from datetime import datetime

def save_output_file(data, filename, output_dir="outputs"):
    """
    Save data to a file in the outputs directory
    """
    # Create outputs directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'w') as file:
        if isinstance(data, str):
            file.write(data)
        else:
            json.dump(data, file, indent=2)
            
    return file_path

def get_available_industries():
    """
    Get list of available industry templates
    """
    industries = ["general"]
    template_dir = "templates"
    
    if os.path.exists(template_dir):
        for file in os.listdir(template_dir):
            if file.endswith(".json"):
                industry = file.split(".")[0]
                if industry != "general":
                    industries.append(industry)
                    
    return industries

def generate_timestamp():
    """
    Generate timestamp string for filenames
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def sanitize_filename(text):
    """
    Sanitize text for use in filenames
    """
    # Replace spaces and special characters
    return "".join([c if c.isalnum() else "_" for c in text]).strip("_")