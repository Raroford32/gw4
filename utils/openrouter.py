import requests
import logging
from app import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AVAILABLE_MODELS = {
    'claude-2': 'anthropic/claude-2',
    'qwen-coder': 'qwen/qwen-2.5-coder-32b-instruct',
    'gpt-3.5': 'openai/gpt-3.5-turbo'
}

def generate_code(message, model='claude-2'):
    try:
        headers = {
            "Authorization": f"Bearer {app.config['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        You are a code generation assistant. Based on the following message, generate a complete code implementation.
        Format the response with clear file paths and content using this structure:
        
        ## file_path: filename.ext
        ```language
        code content
        ```
        
        User Message:
        {message}
        
        Please ensure each file is properly marked with the file path and formatted code blocks.
        If the implementation requires multiple files, provide them all in the specified format.
        """
        
        logger.info(f"Sending request to OpenRouter API using model: {model}")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": AVAILABLE_MODELS.get(model, AVAILABLE_MODELS['claude-2']),
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4000
            }
        )
        
        if response.status_code != 200:
            error_msg = f"API Error: {response.text}"
            logger.error(error_msg)
            return {'error': error_msg}
            
        result = response.json()
        logger.info("Received response from OpenRouter API")
        
        generated_text = result['choices'][0]['message']['content']
        logger.debug(f"Generated text length: {len(generated_text)}")
        
        # Ensure the response has at least one file structure
        if "## file_path:" not in generated_text:
            generated_text = """## file_path: main.py
```python
# Generated code
{generated_text}
```"""
        
        return {
            'code': generated_text
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in generate_code: {error_msg}")
        return {'error': error_msg}
