# Configuration Guide

This guide covers configuration options for AI agents across all categories.

## Table of Contents

- [Environment Configuration](#environment-configuration)
- [API Configuration](#api-configuration)
- [Model Configuration](#model-configuration)
- [Performance Tuning](#performance-tuning)
- [Security Best Practices](#security-best-practices)

## Environment Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
HUGGINGFACE_API_KEY=hf_...
GOOGLE_API_KEY=...

# Model Settings
DEFAULT_MODEL=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=2048

# System Settings
LOG_LEVEL=INFO
CACHE_ENABLED=true
CACHE_DIR=.cache
TIMEOUT=30

# Resource Limits
MAX_WORKERS=4
MEMORY_LIMIT=8GB
GPU_MEMORY_FRACTION=0.8
```

### Configuration Files

#### Global Configuration (`config.yaml`)

```yaml
global:
  log_level: INFO
  cache_enabled: true
  timeout: 30

models:
  default_provider: openai
  providers:
    openai:
      model: gpt-4
      temperature: 0.7
      max_tokens: 2048
    anthropic:
      model: claude-3-sonnet
      temperature: 0.7
      max_tokens: 4096

performance:
  max_workers: 4
  batch_size: 10
  gpu_enabled: true
  gpu_memory_fraction: 0.8
```

## API Configuration

### OpenAI Configuration

```python
# config/openai_config.py
OPENAI_CONFIG = {
    'api_key': os.getenv('OPENAI_API_KEY'),
    'model': 'gpt-4',
    'temperature': 0.7,
    'max_tokens': 2048,
    'top_p': 1,
    'frequency_penalty': 0,
    'presence_penalty': 0,
}
```

### Anthropic Configuration

```python
# config/anthropic_config.py
ANTHROPIC_CONFIG = {
    'api_key': os.getenv('ANTHROPIC_API_KEY'),
    'model': 'claude-3-sonnet-20240229',
    'max_tokens': 4096,
    'temperature': 0.7,
}
```

### Hugging Face Configuration

```python
# config/huggingface_config.py
HUGGINGFACE_CONFIG = {
    'api_key': os.getenv('HUGGINGFACE_API_KEY'),
    'model': 'meta-llama/Llama-2-7b-chat-hf',
    'cache_dir': '.cache/huggingface',
    'local_files_only': False,
}
```

## Model Configuration

### Programming Agents

```yaml
# config/programming.yaml
code_generation:
  model: gpt-4
  temperature: 0.2  # Low for deterministic output
  max_tokens: 4096
  
code_review:
  model: claude-3-sonnet
  temperature: 0.3
  max_tokens: 2048

test_generation:
  model: gpt-3.5-turbo
  temperature: 0.5
  max_tokens: 2048
```

### Document Processing Agents

```yaml
# config/document_processing.yaml
summarization:
  model: gpt-4
  temperature: 0.5
  max_tokens: 1024
  
extraction:
  model: gpt-3.5-turbo
  temperature: 0.2
  max_tokens: 2048

translation:
  model: gpt-4
  temperature: 0.3
  max_tokens: 4096
```

### Image Processing Agents

```yaml
# config/image_processing.yaml
generation:
  model: stable-diffusion-xl
  steps: 50
  guidance_scale: 7.5
  
analysis:
  model: clip-vit-large
  batch_size: 8
  
enhancement:
  model: real-esrgan
  scale: 4
```

## Performance Tuning

### Memory Optimization

```python
# config/performance.py
MEMORY_CONFIG = {
    # Model quantization
    'use_8bit': True,
    'use_4bit': False,
    
    # Batch processing
    'batch_size': 8,
    'prefetch_factor': 2,
    
    # Caching
    'cache_enabled': True,
    'cache_size': '2GB',
    'cache_ttl': 3600,
}
```

### GPU Configuration

```python
GPU_CONFIG = {
    'enabled': True,
    'device': 'cuda:0',
    'memory_fraction': 0.8,
    'allow_growth': True,
    'mixed_precision': True,
}
```

### Parallelization

```python
PARALLEL_CONFIG = {
    'max_workers': 4,
    'thread_pool_size': 8,
    'process_pool_size': 4,
    'async_enabled': True,
}
```

## Security Best Practices

### API Key Management

```python
# Never hardcode API keys
# ❌ Bad
api_key = "sk-abc123..."

# ✅ Good
api_key = os.getenv('OPENAI_API_KEY')

# ✅ Better - with validation
from dotenv import load_dotenv
load_dotenv()

def get_api_key(service):
    key = os.getenv(f'{service.upper()}_API_KEY')
    if not key:
        raise ValueError(f"{service} API key not found")
    return key
```

### Input Validation

```python
# Always validate and sanitize inputs
def validate_input(text, max_length=10000):
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    if len(text) > max_length:
        raise ValueError(f"Input exceeds maximum length of {max_length}")
    return text.strip()
```

### Rate Limiting

```python
# Implement rate limiting
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)
def call_api(prompt):
    # API call implementation
    pass
```

### Data Privacy

```python
# Sanitize sensitive data
import re

def sanitize_data(text):
    # Remove email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    # Remove phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    # Remove credit cards
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD]', text)
    return text
```

## Agent-Specific Configuration

### Programming Agents
See: `config/programming/`

### Document Processing Agents
See: `config/document-processing/`

### Image Processing Agents
See: `config/image-processing/`

### Other Agents
See: `config/other/`

## Configuration Templates

Template files are available in the `templates/` directory:
- `config_template.yaml` - General configuration template
- `env_template` - Environment variables template
- `docker_config_template.yaml` - Docker configuration

## Validation

Validate your configuration:

```bash
python scripts/validate_config.py
```

## Next Steps

- Review [Installation Guide](../installation/README.md)
- Explore [Examples](../../examples/)
- Read agent-specific documentation
- Check [Best Practices](best-practices.md)
