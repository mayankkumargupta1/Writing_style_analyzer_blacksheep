import requests
import json
import os

# Replace with your actual API key
API_KEY = os.getenv("API_KEY") 

async def send_prompt_to_gemini(prompt : str) -> str:
    # Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    # Request headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""
correct grammatical errors and give me a list of changes that can improve the text in this format, just do as said dont include md format or any other text
        Corrected_text:
        TEXT
        Improvements:
        first_improvement | second_improvement | third_improvement | so on
        your text is "{prompt}"
"""
                    }
                ]
            }
        ]
    }
    
    try:
        # Send the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response
        response_json = response.json()
        
        # Extract and return the generated text
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "No response generated."
            
    except requests.exceptions.RequestException as e:
        return f"Error making request to Gemini API: {str(e)}"

if __name__ == "__main__":
    # Get user input
    user_prompt = """
        
    """
    
    # Send the prompt and get the response
    gemini_response = send_prompt_to_gemini(user_prompt)