# Agent Script Template

This template provides a standard structure for creating new AI agent scripts.

## File: `agent_name.py`

```python
#!/usr/bin/env python3
"""
Agent Name: [Your Agent Name]
Category: [programming|document-processing|image-processing|other]
Description: [Brief description of what this agent does]

Author: [Your Name]
Date: [Creation Date]
Version: 1.0.0
"""

import os
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentName:
    """
    [Agent Name] - [Brief Description]
    
    This agent [detailed description of functionality and use cases].
    
    Attributes:
        model (str): The AI model to use
        config (dict): Configuration parameters
        
    Examples:
        >>> agent = AgentName(model="gpt-4")
        >>> result = agent.process(input_data)
        >>> print(result)
    """
    
    def __init__(
        self,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the agent.
        
        Args:
            model: Model identifier (e.g., "gpt-4", "claude-3")
            api_key: API key for the model provider
            **kwargs: Additional configuration parameters
        """
        self.model = model
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.config = self._load_config(kwargs)
        
        # Validate configuration
        self._validate_setup()
        
        logger.info(f"Initialized {self.__class__.__name__} with model: {model}")
    
    def _load_config(self, kwargs: Dict) -> Dict:
        """Load and merge configuration."""
        default_config = {
            'temperature': 0.7,
            'max_tokens': 2048,
            'timeout': 30,
        }
        return {**default_config, **kwargs}
    
    def _validate_setup(self):
        """Validate that all required setup is complete."""
        if not self.api_key:
            raise ValueError(
                "API key not found. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
    
    def process(
        self,
        input_data: Any,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Main processing method.
        
        Args:
            input_data: Input data to process
            **kwargs: Additional processing parameters
            
        Returns:
            Dictionary containing:
                - output: Processed result
                - metadata: Processing metadata
                - status: Success/failure status
                
        Raises:
            ValueError: If input data is invalid
            RuntimeError: If processing fails
            
        Examples:
            >>> agent = AgentName()
            >>> result = agent.process("input text")
            >>> print(result['output'])
        """
        try:
            # Validate input
            self._validate_input(input_data)
            
            # Process
            logger.info("Starting processing...")
            output = self._execute_processing(input_data, **kwargs)
            
            # Prepare result
            result = {
                'output': output,
                'metadata': self._get_metadata(),
                'status': 'success'
            }
            
            logger.info("Processing completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            return {
                'output': None,
                'error': str(e),
                'status': 'failed'
            }
    
    def _validate_input(self, input_data: Any):
        """Validate input data."""
        if input_data is None:
            raise ValueError("Input data cannot be None")
        # Add more validation as needed
    
    def _execute_processing(self, input_data: Any, **kwargs) -> Any:
        """
        Execute the main processing logic.
        
        Override this method with your specific implementation.
        """
        # TODO: Implement processing logic
        raise NotImplementedError("Processing logic not implemented")
    
    def _get_metadata(self) -> Dict:
        """Get processing metadata."""
        return {
            'model': self.model,
            'version': '1.0.0',
            'config': self.config
        }
    
    def batch_process(
        self,
        inputs: List[Any],
        parallel: bool = False,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Process multiple inputs.
        
        Args:
            inputs: List of inputs to process
            parallel: Whether to process in parallel
            **kwargs: Additional processing parameters
            
        Returns:
            List of results for each input
        """
        logger.info(f"Batch processing {len(inputs)} items...")
        
        if parallel:
            return self._parallel_process(inputs, **kwargs)
        else:
            return [self.process(item, **kwargs) for item in inputs]
    
    def _parallel_process(self, inputs: List[Any], **kwargs) -> List[Dict]:
        """Process inputs in parallel."""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_input = {
                executor.submit(self.process, inp, **kwargs): inp 
                for inp in inputs
            }
            
            for future in as_completed(future_to_input):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Parallel processing error: {e}")
                    results.append({
                        'output': None,
                        'error': str(e),
                        'status': 'failed'
                    })
        
        return results


def main():
    """Command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description='[Agent Description]')
    parser.add_argument('input', help='Input data or file path')
    parser.add_argument('--model', default='gpt-4', help='Model to use')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--batch', action='store_true', help='Batch mode')
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = AgentName(model=args.model)
    
    # Process
    if args.batch:
        # Load batch inputs
        inputs = []  # TODO: Load from file
        results = agent.batch_process(inputs)
    else:
        result = agent.process(args.input)
        print(result)
    
    # Save output if specified
    if args.output:
        # TODO: Save results to file
        pass


if __name__ == '__main__':
    main()
```

## Testing Template

Create `test_agent_name.py`:

```python
import pytest
from agent_name import AgentName


class TestAgentName:
    """Test suite for AgentName."""
    
    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return AgentName(model="gpt-4", api_key="test_key")
    
    def test_initialization(self, agent):
        """Test agent initialization."""
        assert agent.model == "gpt-4"
        assert agent.api_key == "test_key"
    
    def test_process(self, agent):
        """Test basic processing."""
        result = agent.process("test input")
        assert result['status'] in ['success', 'failed']
    
    def test_invalid_input(self, agent):
        """Test error handling for invalid input."""
        result = agent.process(None)
        assert result['status'] == 'failed'
    
    def test_batch_process(self, agent):
        """Test batch processing."""
        inputs = ["input1", "input2", "input3"]
        results = agent.batch_process(inputs)
        assert len(results) == len(inputs)


if __name__ == '__main__':
    pytest.main([__file__])
```

## Documentation Template

Create `agent_name.md`:

```markdown
# Agent Name

## Overview

Brief description of the agent's purpose and capabilities.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

\```bash
pip install -r requirements.txt
\```

## Usage

### Basic Example

\```python
from agent_name import AgentName

agent = AgentName(model="gpt-4")
result = agent.process("input data")
print(result)
\```

### Advanced Example

\```python
# More complex usage example
\```

## Configuration

Available configuration options:

- `model`: AI model to use
- `temperature`: Creativity level (0.0-1.0)
- `max_tokens`: Maximum output length

## API Reference

### AgentName

Main agent class.

#### Methods

- `process(input_data)`: Process single input
- `batch_process(inputs)`: Process multiple inputs

## Performance

- Speed: [metrics]
- Memory: [requirements]
- GPU: [requirements/optional]

## Limitations

- Limitation 1
- Limitation 2

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md)

## License

MIT License - see [LICENSE](../../LICENSE)
```

## Requirements Template

Create `requirements.txt`:

```txt
# Core dependencies
openai>=1.0.0
anthropic>=0.7.0
python-dotenv>=1.0.0

# Processing
pydantic>=2.0.0
requests>=2.31.0

# Utilities
tqdm>=4.66.0
click>=8.1.0

# Development
pytest>=7.4.0
black>=23.0.0
flake8>=6.1.0
```

## Next Steps

1. Copy this template
2. Rename files appropriately
3. Implement the `_execute_processing` method
4. Add tests
5. Update documentation
6. Submit pull request
