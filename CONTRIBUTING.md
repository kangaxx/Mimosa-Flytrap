# Contributing to Mimosa-Flytrap

Thank you for your interest in contributing to Mimosa-Flytrap! This document provides guidelines for contributing AI agents, documentation, and improvements to this repository.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Agent Contribution Guidelines](#agent-contribution-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists
2. Create a new issue with a clear title and description
3. Include relevant details:
   - Agent category
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Enhancements

For new features or improvements:

1. Open an issue describing the enhancement
2. Explain the use case and benefits
3. Include examples if applicable
4. Wait for feedback before starting work

## Agent Contribution Guidelines

### Adding a New Agent

1. **Choose the Right Category**
   - `agents/programming/` - Code-related tasks
   - `agents/document-processing/` - Document analysis/transformation
   - `agents/image-processing/` - Image generation/analysis
   - `agents/other/` - Everything else

2. **Use the Agent Template**
   ```bash
   cp templates/agent-template.md agents/[category]/your_agent.py
   ```

3. **Required Components**
   - Main agent script
   - Documentation (README or .md file)
   - Example usage
   - Requirements file (if needed)
   - Tests (recommended)

4. **Agent Script Requirements**
   - Follow the template structure
   - Include docstrings
   - Add error handling
   - Implement logging
   - Support batch processing (if applicable)

5. **Testing**
   - Write unit tests
   - Test with various inputs
   - Verify error handling
   - Check edge cases

### Agent Quality Standards

Your agent should:
- Have a clear, specific purpose
- Be well-documented
- Handle errors gracefully
- Include usage examples
- Follow Python best practices
- Be efficient and performant

### Example Agent Structure

```
agents/
└── programming/
    ├── code_reviewer/
    │   ├── __init__.py
    │   ├── code_reviewer.py
    │   ├── README.md
    │   ├── requirements.txt
    │   └── tests/
    │       └── test_code_reviewer.py
    └── README.md (updated with new agent)
```

## Documentation Guidelines

### Documentation Types

1. **Agent Documentation**
   - Purpose and features
   - Installation instructions
   - Usage examples
   - Configuration options
   - API reference
   - Performance notes
   - Limitations

2. **Installation Guides**
   - Step-by-step instructions
   - Environment-specific details
   - Troubleshooting tips

3. **Examples**
   - Working code samples
   - Various use cases
   - Best practices

### Writing Style

- Use clear, concise language
- Include code examples
- Add comments for complex code
- Use proper markdown formatting
- Check spelling and grammar

### Updating Documentation

When contributing:
- Update relevant README files
- Add examples to examples directory
- Update configuration docs if needed
- Keep documentation synchronized with code

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/your-username/Mimosa-Flytrap.git
cd Mimosa-Flytrap
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Create Branch

```bash
git checkout -b feature/your-feature-name
```

## Pull Request Process

### Before Submitting

1. **Test Your Changes**
   ```bash
   pytest tests/
   ```

2. **Check Code Style**
   ```bash
   black .
   flake8 .
   ```

3. **Update Documentation**
   - Update relevant README files
   - Add examples if needed
   - Update CHANGELOG.md

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

### Submitting PR

1. Push to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create Pull Request on GitHub
   - Use a clear title
   - Describe what and why
   - Reference related issues
   - Add screenshots if applicable

3. PR Template
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] New agent
   - [ ] Bug fix
   - [ ] Documentation update
   - [ ] Enhancement
   
   ## Agent Category
   - [ ] Programming
   - [ ] Document Processing
   - [ ] Image Processing
   - [ ] Other
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] Examples provided
   - [ ] Self-review completed
   
   ## Testing
   Describe testing performed
   
   ## Screenshots (if applicable)
   ```

### Review Process

1. Maintainers will review your PR
2. Address feedback and requested changes
3. Once approved, PR will be merged

## Style Guidelines

### Python Code Style

- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters (Black default)
- Use descriptive variable names
- Add docstrings to functions and classes

### Example Good Code

```python
from typing import Dict, List, Optional

def process_documents(
    documents: List[str],
    max_length: int = 1000,
    language: Optional[str] = None
) -> Dict[str, str]:
    """
    Process a list of documents.
    
    Args:
        documents: List of document texts
        max_length: Maximum document length
        language: Target language for processing
        
    Returns:
        Dictionary mapping document IDs to processed text
    """
    results = {}
    for idx, doc in enumerate(documents):
        if len(doc) <= max_length:
            results[f"doc_{idx}"] = doc
    return results
```

### Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

Examples:
```
feat: add document summarization agent
fix: resolve GPU memory leak in image processor
docs: update installation guide for macOS
```

## Agent Categories

### Programming Agents
Focus on code generation, analysis, and transformation.

### Document Processing Agents
Handle text extraction, analysis, and document manipulation.

### Image Processing Agents
Work with image generation, analysis, and transformation.

### Other Agents
Anything that doesn't fit the above categories.

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues for similar questions

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in agent documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Mimosa-Flytrap! 🌺
