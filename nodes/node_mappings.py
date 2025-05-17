
from .ollama import (
    OllamaVision,
    OllamaGenerateAdvance,
    OllamaOptionsV2,
    OllamaGenerate,
    OllamaConnectivityV2,
    OllamaGenerateV2,
    OllamaSaveContext,
    OllamaLoadContext,
)

from .bcknt import (
    SystemPromptLoader,
    ActionPromptLoader,
    CleanResponse,
    BaseAgent
    
)

NODE_CLASS_MAPPINGS = {
    #Agents
    "bcknt_agent": BaseAgent,
    # Utils
    "bcknt_prompt_context_loader": SystemPromptLoader,
    "bcknt_prompt_loader": ActionPromptLoader,
    "bcknt_clean_response": CleanResponse,
    
    # Ollama nodes
    "BckntOllamaVision": OllamaVision,
    "BckntOllamaGenerateAdvance": OllamaGenerateAdvance,
    "BckntOllamaOptionsV2": OllamaOptionsV2,
    "BckntOllamaGenerate": OllamaGenerate,
    "BckntOllamaConnectivityV2": OllamaConnectivityV2,
    "BckntOllamaGenerateV2": OllamaGenerateV2,
    "BckntOllamaSaveContext": OllamaSaveContext,
    "BckntOllamaLoadContext": OllamaLoadContext,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # Agents
    "bcknt_agent": "🧑‍💻Agent",
    # Utils
    "bcknt_prompt_context_loader": "📑Prompt Context Loader",
    "bcknt_prompt_loader": "📑Prompt Loader",
    "bcknt_clean_response": "🧼Clean Response",
    
    # Ollama nodes
    "BckntOllamaVision": "Ollama Vision",
    "BckntOllamaGenerate": "Ollama Generate",
    "BckntOllamaGenerateAdvance": "Ollama Generate Advance",
    "BckntOllamaOptionsV2": "Ollama Options V2",
    "BckntOllamaConnectivityV2": "Ollama Connectivity V2",
    "BckntOllamaGenerateV2": "Ollama Generate V2",
    "BckntOllamaSaveContext": "Ollama Save Context",
    "BckntOllamaLoadContext": "Ollama Load Context",
}
