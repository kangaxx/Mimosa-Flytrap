"""
Sample Code Generator Agent

This is a sample implementation to demonstrate the structure of an agent in this repository.
For a complete template, see: templates/agent-template.md
"""

import os
from typing import Optional, Dict, Any


class SampleCodeGenerator:
    """
    Sample code generation agent.
    
    This is a minimal example showing the basic structure of an agent.
    In practice, this would integrate with actual AI APIs (OpenAI, Anthropic, etc.)
    
    Example:
        >>> generator = SampleCodeGenerator()
        >>> code = generator.generate("Create a hello world function")
        >>> print(code)
    """
    
    def __init__(self, model: str = "gpt-4", api_key: Optional[str] = None):
        """
        Initialize the code generator.
        
        Args:
            model: AI model to use
            api_key: API key for the AI service
        """
        self.model = model
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate code from a text prompt.
        
        Args:
            prompt: Description of the code to generate
            **kwargs: Additional parameters
            
        Returns:
            Generated code as a string
        """
        # This is a placeholder implementation
        # In practice, this would call an actual AI API
        
        return f'''def hello_world():
    """
    Sample generated function based on: {prompt}
    """
    print("Hello, World!")
    return "Generated code"
'''


# Example usage
if __name__ == '__main__':
    generator = SampleCodeGenerator()
    code = generator.generate("Create a hello world function")
    print("Generated code:")
    print(code)
