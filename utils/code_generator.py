import re
import logging

logger = logging.getLogger(__name__)

def process_generation(generated_text):
    """Process the generated code and extract file information"""
    files = []
    
    try:
        # More robust pattern to match file paths and their content
        file_pattern = r'##\s*file_path\s*:\s*([^\n]+)\n```[^\n]*\n(.*?)```'
        
        # Find all matches in the generated text
        matches = re.finditer(file_pattern, generated_text, re.DOTALL)
        
        for match in matches:
            file_path = match.group(1).strip()
            content = match.group(2).strip()
            files.append({
                'path': file_path,
                'content': content
            })
        
        # If no files were found, create a default file with the raw text
        if not files:
            logger.warning("No file structure detected in generated text")
            files.append({
                'path': 'generated_code.txt',
                'content': generated_text.strip()
            })
        
        logger.info(f"Processed {len(files)} files from generated text")
        return files
        
    except Exception as e:
        logger.error(f"Error processing generated text: {str(e)}")
        # Return a default file with error message
        return [{
            'path': 'error.txt',
            'content': f"Error processing generated code:\n{str(e)}\n\nRaw generated text:\n{generated_text}"
        }]
