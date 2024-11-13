import requests
from app import app

def generate_code(requirements, specifications):
    try:
        headers = {
            "Authorization": f"Bearer {app.config['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        Requirements:
        {requirements}
        
        Specifications:
        {specifications}
        
        Please generate the complete code implementation following these requirements and specifications.
        Provide the code in a structured format with clear file paths and content.
        """
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "anthropic/claude-2",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4000
            }
        )
        
        if response.status_code != 200:
            return {'error': f"API Error: {response.text}"}
            
        result = response.json()
        generated_text = result['choices'][0]['message']['content']
        
        return {
            'code': generated_text
        }
        
    except Exception as e:
        return {'error': str(e)}
