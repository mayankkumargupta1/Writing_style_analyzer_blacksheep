from blacksheep.server.controllers import Controller, get, post
from blacksheep import Request
from domain.gemmini import send_prompt_to_gemini

class Home(Controller):
    @get()
    def index(self):
        return self.view()
        
    @post()
    async def correct_grammar(self, request: Request):
        form = await request.form()
        user_text = form.get("user_text", "").strip()
        
        if not user_text:
            return self.view("results", 
                          corrected_text="",
                          improvements=["Please enter some text to correct"])
        
        try:
            # Get response from Gemini
            gemini_response = await send_prompt_to_gemini(user_text)
            
            # Parse the response
            corrected_text = "Could not parse corrected text"
            improvements = ["No improvements found"]
            
            if "Corrected_text:" in gemini_response:
                corrected_part = gemini_response.split("Corrected_text:")[1]
                corrected_text = corrected_part.split("Improvements:")[0].strip()
                
                if "Improvements:" in corrected_part:
                    improvements = [
                        imp.strip() 
                        for imp in corrected_part.split("Improvements:")[1].split("|")
                        if imp.strip()
                    ]
            
            return self.view("results",
                            corrected_text=corrected_text,
                            improvements=improvements)
            
        except Exception as e:
            return self.view("results",
                          corrected_text="Error",
                          improvements=[f"Failed to process: {str(e)}"])