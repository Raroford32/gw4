import re

def process_generation(generated_text):
    """Process the generated code and extract file information"""
    files = []
    
    # Pattern to match file paths and their content
    file_pattern = r'## file_path: ([^\n]+)\n```[^\n]*\n(.*?)```'
    
    # Find all matches in the generated text
    matches = re.finditer(file_pattern, generated_text, re.DOTALL)
    
    for match in matches:
        file_path = match.group(1).strip()
        content = match.group(2).strip()
        files.append({
            'path': file_path,
            'content': content
        })
    
    return files
