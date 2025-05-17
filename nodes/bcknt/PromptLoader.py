from .prompt_paths import SYSTEM_AGENT_PROMPTS_PATH, PROMPT_AGENT_PROMPTS_PATH
import os
class PromptLoader: 
    def __init__(self, path):
        self.path = path
        self.prompt = ""
        self.system = ""
    
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
            },
            "optional": {
                "task": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Define the task to be performed by the specialist."
                }),
                "model": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "tooltip": "Define the model to be used by the specialist."
                }),
                "positive_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Define the positive guidelines for the specialist.",
                    "title": "Positive Prompt"
                }),
                "negative_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Define the negative guidelines for the specialist."
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("system", "prompt",)
    FUNCTION = "run"
    
    CATEGORY = "BlackNightTales/utils"
        
    def load_prompt(self,  file_name):
        """
        Load a prompt from a text file.
        
        Args:
            text_file_path (str): Path to the text file containing the prompt.
            base_path (str): Base path to prepend to the text file path.
        
        Returns:
            str: The loaded prompt.
        """
        

        file_path = f"{file_name}.txt"
        full_path = os.path.join(self.path, file_path )
        prompt = ""
        if not os.path.exists(full_path):
            return ''
        with open(full_path, 'r') as f:
            prompt = f.read()
            
        
        return prompt
    
    def replace_prompt(self, prompt, **args):
        """
        Replace the prompt with the new task and guidelines.
        
        Args:
            task (str): The new task to be performed by the specialist.
            positive_guidelines (str): The new positive guidelines for the specialist.
            negative_guidelines (str): The new negative guidelines for the specialist.
        
        Returns:
            str: The updated prompt.
        """
        
        # Replace the placeholders in the prompt with the new values
        for key, value in args.items():
            if value:
                prompt = prompt.replace(f"[{key}]", value)
            else:
                prompt = prompt.replace(f"[{key}]", "")
        
        return prompt
    
    
    def run (self, **args):
        """
        Run the specialist with the given task and guidelines.
        
        Args:
            task (str): The task to be performed by the specialist.
            context_type (bool): If true, the prompt will be loaded as a context.
            positive_guidelines (str): The positive guidelines for the specialist.
            negative_guidelines (str): The negative guidelines for the specialist.
        
        Returns:
            str: The final prompt after replacing the placeholders.
        """
        
        # Load the prompt
        self.prompt = self.load_prompt("prompt")
        self.system = self.load_prompt("context")

        self.prompt = self.replace_prompt(self.prompt, **args)
        self.system = self.replace_prompt(self.system, **args)
        
        return (self.system, self.prompt, )
    
class SystemPromptLoader(PromptLoader):
    def __init__(self):
        super().__init__(SYSTEM_AGENT_PROMPTS_PATH) 
    

    DESCRIPTION = "Load a context specialist"
    
class ActionPromptLoader(PromptLoader):
    def __init__(self):
        super().__init__(PROMPT_AGENT_PROMPTS_PATH) 
    

    DESCRIPTION = "Load a prompt specialist"