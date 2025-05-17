import pytest

from nodes.bcknt import (BaseAgent)


@pytest.fixture
def base_agent_node():
    """Fixture to create a BaseAgent node instance."""
    return BaseAgent()


def base_options():
    return {

            "enable_mirostat": False,
            "mirostat": 0,
            "enable_mirostat_eta": False,
            "mirostat_eta": 0.1,
            "enable_mirostat_tau": False,
            "mirostat_tau": 5.0,
            "enable_num_ctx": False,
            "num_ctx": 2048,
            "enable_repeat_last_n": False,
            "repeat_last_n": 64,
            "enable_repeat_penalty": False,
            "repeat_penalty": 1.1,
            "enable_temperature": False,
            "temperature": 0.8,
            "enable_seed": False,
            "seed": 1,  # Note: 'seed' variable needs to be defined
            "enable_stop": False,
            "stop": "",
            "enable_tfs_z": False,
            "tfs_z": 1,
            "enable_num_predict": False,
            "num_predict": -1,
            "enable_top_k": False,
            "top_k": 40,
            "enable_top_p": False,
            "top_p": 0.9,
            "enable_min_p": False,
            "min_p": 0.0,
            "debug": False,   
        
    }
    
def connectivity_options():
    return {
        "url": "http://localhost:11434",
        "model": "mistral-nemo:latest",
        "keep_alive": 1,
        "keep_alive_unit": "minutes",
        
    }
def generate_options():
    return {

        "keep_context": False,
        "format": "text",
    }
     

def test_base_agent_node_initialization(base_agent_node):
    """Test that the node can be instantiated."""
    assert isinstance(base_agent_node, BaseAgent)

    assert base_agent_node.CATEGORY == "BlackNightTales/Agents"


def test_base_agent_execution(base_agent_node):
    """Test the node's execution."""
    # Define test inputs
    

    # Execute the node
    response = base_agent_node.run_agent(**{**connectivity_options(), **generate_options(), **base_options()})

    # Check the response
    # assert isinstance(response, tuple)
        