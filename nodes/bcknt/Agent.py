from ..ollama import (
    OllamaOptionsV2,
    OllamaConnectivityV2,
    OllamaGenerateV2
)
from . import (
    CleanResponse,
    ActionPromptLoader,
    SystemPromptLoader
)

from ..utils.merge_input_types import  merge_input_types

from .MultiNodeExecutor import MultiNodeExecutor

    
class BaseAgent:
    _fine_tune = False
    
    def __init__(self, options=None):
        self.model_options = options

            
    @classmethod 
    def set_fine_tune(cls, fine_tune):
        cls._fine_tune = fine_tune
        
    @classmethod
    def is_fine_tune(cls):
        return cls._fine_tune
        
        
    
    @classmethod
    def INPUT_TYPES(cls):
        connectivity_inputs = OllamaConnectivityV2.INPUT_TYPES()
        generate_inputs = OllamaGenerateV2.INPUT_TYPES()
        options_inputs = OllamaOptionsV2.INPUT_TYPES()
        system_inputs = SystemPromptLoader.INPUT_TYPES()
        action_inputs = ActionPromptLoader.INPUT_TYPES()
        
        generate_inputs = MultiNodeExecutor.remove_inputs(generate_inputs, ['system', 'prompt'])
        system_inputs = MultiNodeExecutor.remove_inputs(system_inputs, [ 'model'])
        action_inputs = MultiNodeExecutor.remove_inputs(action_inputs, [ 'model'])
        is_fine_tune = cls.is_fine_tune()
        inputs = [
            system_inputs,
            action_inputs,
            connectivity_inputs,
            generate_inputs,
        ]
        
        inputs = inputs + [options_inputs] if is_fine_tune else inputs 
        inputs = merge_input_types(inputs)
        return inputs
    
    RETURN_TYPES = ("STRING","STRING", "STRING")
    RETURN_NAMES = ("response", "system", "prompt")
    CATEGORY = "BlackNightTales/Agents"
    FUNCTION = "run_agent"
    
    def run_agent(self, **kwargs):
        print("SELF OPTIONS:", self.model_options)
        ollama_options = self.get_default_options(OllamaOptionsV2) if self.model_options is None else self.model_options
        print ("Ollama options:", ollama_options)
        node_configs = [
            {'node': OllamaConnectivityV2},
            {'node': SystemPromptLoader, 'inputs': {'model': 'my custom model'}},
            {'node': ActionPromptLoader, 'inputs': {'model': ('my custom model 2',)}},
            {'node': OllamaOptionsV2, 'fixed_kwargs': ollama_options},
            {
                'node': OllamaGenerateV2,
                'inputs': [
                    ('SystemPromptLoader', 'system'),
                    ('ActionPromptLoader', 'prompt'),
                    ('OllamaConnectivityV2', [('connection', 'connectivity')]),
                    ('OllamaOptionsV2', 'options')
                ]
            },
            {
                'node': CleanResponse,
                'inputs': [
                    ('OllamaGenerateV2', [('result', 'model_response')]),
                ]
            }
        ]

        executor = MultiNodeExecutor(node_configs)
        results = executor.execute_nodes(**kwargs)

        return (results['CleanResponse'], results['SystemPromptLoader'], results['ActionPromptLoader'])
        
    
    def get_default_options(self, node):
        options = node.INPUT_TYPES()
        default_options = {}
        if 'required' in options:
            
            for key, value in options['required'].items():
                if 'default' in value[1]:
                    default_options[key] = value[1]['default']
        if 'optional' in options:
            for key, value in options['optional'].items():
                if 'default' in value[1]:
                    default_options[key] = value[1]['default']
        return default_options
        
   
        
        
        
    
    
    
        
