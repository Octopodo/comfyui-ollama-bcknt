#!/usr/bin/env python

"""Tests for `black_night_tales_nodes` package."""

import pytest
from nodes.bcknt import SystemPromptLoader, CleanResponse


@pytest.fixture
def system_prompt_loader_node():
    """Fixture to create an Example node instance."""
    return SystemPromptLoader()

def test_example_node_initialization(system_prompt_loader_node):
    """Test that the node can be instantiated."""
    assert isinstance(system_prompt_loader_node, SystemPromptLoader)

def test_return_types():
    """Test the node's metadata."""
    assert SystemPromptLoader.RETURN_TYPES == ("STRING", "STRING")
    assert SystemPromptLoader.RETURN_NAMES == ("system", "prompt")
    assert SystemPromptLoader.FUNCTION == "run"
    assert SystemPromptLoader.CATEGORY == "BlackNightTales/utils"



@pytest.fixture
def clean_response_node():
    """Fixture to create an Example node instance."""
    return CleanResponse()

def test_clean_response_node_initialization(clean_response_node):
    """Test that the node can be instantiated."""
    assert isinstance(clean_response_node, CleanResponse)
    
def test_clean_response_return_types():
    """Test the node's metadata."""
    assert CleanResponse.RETURN_TYPES == ("STRING",)
    assert CleanResponse.RETURN_NAMES == ("cleaned_response",)
    assert CleanResponse.FUNCTION == "clean_response"
    assert CleanResponse.CATEGORY == "BlackNightTales/utils"
    
    
def test_clean_response_function(clean_response_node):
    """Test the clean_response function."""
    test_response = "<think> This is a test </think> <thinking> This is another test </thinking> This is the cleanded respone"
    expected_cleaned_response = "This is the cleanded respone"
    
    cleaned_response = clean_response_node.clean_response(test_response)
    
    assert cleaned_response == (expected_cleaned_response,)
    
def test_clean_respones_return_types(clean_response_node):
    """Test the clean_response function return types."""
    test_response = "<think> This is a test </think> <thinking> This is another test </thinking> This is the cleanded respone"
    
    cleaned_response = clean_response_node.clean_response(test_response)
    
    assert isinstance(cleaned_response, tuple)
    assert len(cleaned_response) == 1
    assert isinstance(cleaned_response[0], str)