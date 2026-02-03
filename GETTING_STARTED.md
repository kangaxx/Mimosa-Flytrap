# Getting Started with Mimosa-Flytrap

Welcome to Mimosa-Flytrap! This guide will help you get started with using AI agents for your projects.

## Quick Start (5 Minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/kangaxx/Mimosa-Flytrap.git
cd Mimosa-Flytrap
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Create .env file with your API keys
cat > .env << EOF
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
EOF
```

### 3. Try Your First Agent

Let's try a simple programming agent example:

```python
# Save as test_agent.py
from agents.programming.code_generator import CodeGenerator

# Initialize agent
agent = CodeGenerator(model="gpt-4")

# Generate code
code = agent.generate("Create a function that calculates fibonacci numbers")
print(code)
```

## What Can You Do?

### Programming Tasks
- **Generate code** from descriptions
- **Review code** for issues and improvements
- **Generate tests** automatically
- **Refactor code** to improve quality
- **Generate documentation**

**→ Start with:** `examples/programming/`

### Document Processing
- **Extract text** from PDFs
- **Summarize documents** automatically
- **Translate documents** to other languages
- **Extract entities** (names, dates, locations)
- **Convert formats** (PDF ↔ DOCX ↔ MD)

**→ Start with:** `examples/document-processing/`

### Image Processing
- **Generate images** from text descriptions
- **Detect objects** in images
- **Remove backgrounds** automatically
- **Enhance image** quality
- **Extract text** from images (OCR)

**→ Start with:** `examples/image-processing/`

### Other Tasks
- **Transcribe audio** to text
- **Process videos** and extract information
- **Automate web scraping**
- **Build chatbots**
- **Analyze data** and create visualizations

**→ Start with:** `examples/other/`

## Choose Your Path

### Path 1: I Want to Use Existing Agents

1. Browse `agents/` directory for available agents
2. Check `examples/` for usage demonstrations
3. Copy example code and adapt to your needs
4. Configure in `docs/configuration/`

### Path 2: I Want to Create My Own Agent

1. Read `templates/agent-template.md`
2. Copy template to appropriate category
3. Implement your agent logic
4. Add tests and documentation
5. Submit PR (see `CONTRIBUTING.md`)

### Path 3: I Want to Learn More

1. Read the comprehensive [README.md](README.md)
2. Explore [Installation Guide](docs/installation/README.md)
3. Study [Configuration Guide](docs/configuration/README.md)
4. Check out all examples in `examples/`

## Common Use Cases

### Use Case 1: Code Review Automation

```python
from agents.programming.code_reviewer import CodeReviewer

reviewer = CodeReviewer(model="gpt-4")

# Review your code
review = reviewer.review_file("src/my_module.py")

# Print suggestions
for issue in review.issues:
    print(f"{issue.severity}: {issue.message}")
    print(f"  Line {issue.line}: {issue.suggestion}")
```

### Use Case 2: Document Summarization

```python
from agents.document_processing.summarizer import DocumentSummarizer

summarizer = DocumentSummarizer()

# Summarize a PDF
summary = summarizer.summarize_file(
    "documents/report.pdf",
    max_length=200,
    format="bullet_points"
)

print(summary)
```

### Use Case 3: Image Generation

```python
from agents.image_processing.generator import ImageGenerator

generator = ImageGenerator(model="stable-diffusion-xl")

# Generate image
image = generator.generate(
    prompt="A beautiful sunset over mountains",
    width=1024,
    height=768
)

image.save("output/sunset.png")
```

### Use Case 4: Web Data Extraction

```python
from agents.other.web.scraper import WebScraper

scraper = WebScraper()

# Extract data from website
data = scraper.scrape(
    url="https://example.com",
    selectors={
        "title": "h1",
        "content": ".main-content"
    }
)

print(data)
```

## Configuration Basics

### Environment Variables

Create `.env` file:
```bash
# Required for most agents
OPENAI_API_KEY=sk-...

# Optional for specific agents
ANTHROPIC_API_KEY=sk-ant-...
HUGGINGFACE_API_KEY=hf_...
```

### Configuration Files

Create `config.yaml`:
```yaml
default_model: gpt-4
temperature: 0.7
max_tokens: 2048
timeout: 30
```

## Best Practices

1. **Start Simple**: Try basic examples first
2. **Use Virtual Environments**: Keep dependencies isolated
3. **Secure API Keys**: Never commit them to git
4. **Test Incrementally**: Start with small inputs
5. **Read Examples**: Learn from working code
6. **Check Documentation**: Refer to docs for details

## Troubleshooting

### Problem: "API key not found"
**Solution:** Create `.env` file with your API keys

### Problem: "Module not found"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Problem: "Out of memory"
**Solution:** Reduce batch size or use smaller models

### Problem: "Rate limit exceeded"
**Solution:** Add delays between API calls or upgrade API plan

## Next Steps

### 1. Explore Examples
Browse `examples/` directory and try running examples:
```bash
python examples/programming/01_code_generation.py
```

### 2. Read Documentation
- [Installation Guide](docs/installation/README.md)
- [Configuration Guide](docs/configuration/README.md)
- Category-specific READMEs in each `agents/` subdirectory

### 3. Build Something
Pick a problem you want to solve and use an agent to help!

### 4. Contribute
Found something useful? Share it back:
- Add new agents
- Improve documentation
- Submit bug fixes
- Share examples

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Getting Help

- **Issues**: Open a GitHub issue for bugs
- **Discussions**: Use GitHub Discussions for questions
- **Examples**: Check `examples/` for working code
- **Docs**: Read documentation in `docs/`

## Resources

### Documentation
- [Main README](README.md)
- [Installation](docs/installation/README.md)
- [Configuration](docs/configuration/README.md)
- [Contributing](CONTRIBUTING.md)

### Agent Categories
- [Programming Agents](agents/programming/README.md)
- [Document Processing](agents/document-processing/README.md)
- [Image Processing](agents/image-processing/README.md)
- [Other Agents](agents/other/README.md)

### Examples
- [Programming Examples](examples/programming/README.md)
- [Document Examples](examples/document-processing/README.md)
- [Image Examples](examples/image-processing/README.md)
- [Other Examples](examples/other/README.md)

## Community

- **GitHub**: [kangaxx/Mimosa-Flytrap](https://github.com/kangaxx/Mimosa-Flytrap)
- **License**: MIT License
- **Contributions**: Welcome!

---

**Ready to start?** Pick an example and run it! 🚀
