
import re
class CleanResponse:
    """
    A class to remove thinking text returned by the model
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_response": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "The response to be cleaned.",
                }),
            }
        }
        
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("cleaned_response",)
    
    FUNCTION = "clean_response"
    CATEGORY = "BlackNightTales/utils"
    
    def clean_response(self, model_response):
        """
        Clean the model response by removing thinking text 
        inside the tags <think></think> or <thinking></thinking> by regexp.
        
        Args:
            model_response (str): The response to be cleaned.
        
        Returns:
            str: The cleaned response.
        """

        cleaned_text = re.sub(r"<think>.*?</think>", "", model_response, flags=re.DOTALL)
        cleaned_text = re.sub(r"<thinking>.*?</thinking>", "", cleaned_text, flags=re.DOTALL)
        
        return (cleaned_text.strip(),)
        
