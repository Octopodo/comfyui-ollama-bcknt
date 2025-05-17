

# BASE_PATH = "C:\\work\\black night tales\\prompts"
# CONTEXT_SPECIALIST_PATH = BASE_PATH + "\\generics\\context-specialist"
import os

CURRENT_PATH = os.getcwd()
BASE_PATH = os.path.join(CURRENT_PATH, 'custom_nodes\\black_night_tales_nodes\\src\\prompts\\')
SYSTEM_AGENT_PROMPTS_PATH = os.path.join(BASE_PATH, 'system')
PROMPT_AGENT_PROMPTS_PATH = os.path.join(BASE_PATH, 'prompt')
