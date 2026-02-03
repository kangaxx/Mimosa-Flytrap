# Programming Agent Examples

This directory contains practical examples demonstrating how to use programming agents.

## Basic Examples

### 1. Code Generation

**Example: Generate a REST API endpoint**

```python
from agents.programming.code_generator import CodeGenerator

# Initialize the agent
generator = CodeGenerator(model="gpt-4")

# Generate code
prompt = """
Create a Python FastAPI endpoint that:
- Accepts POST requests at /api/users
- Validates user data (name, email, age)
- Returns created user with 201 status
"""

code = generator.generate(prompt)
print(code)
```

**Output:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator

app = FastAPI()

class User(BaseModel):
    name: str
    email: EmailStr
    age: int
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v

@app.post("/api/users", status_code=201)
async def create_user(user: User):
    # Save user to database (implementation needed)
    return {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }
```

### 2. Code Review

**Example: Review code for issues**

```python
from agents.programming.code_reviewer import CodeReviewer

reviewer = CodeReviewer(model="claude-3-sonnet")

code = """
def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            result.append(data[i] * 2)
    return result
"""

review = reviewer.review(code)
print(review)
```

**Output:**
```
Issues found:
1. Use list comprehension for better performance
2. No input validation
3. No type hints
4. No docstring

Suggested improvement:
def process_data(data: list[int]) -> list[int]:
    """
    Process positive values by doubling them.
    
    Args:
        data: List of integers to process
        
    Returns:
        List of doubled positive integers
    """
    if not isinstance(data, list):
        raise TypeError("data must be a list")
    
    return [x * 2 for x in data if x > 0]
```

### 3. Test Generation

**Example: Generate unit tests**

```python
from agents.programming.test_generator import TestGenerator

generator = TestGenerator(model="gpt-4")

code = """
def calculate_discount(price, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
"""

tests = generator.generate_tests(code, framework="pytest")
print(tests)
```

**Output:**
```python
import pytest
from your_module import calculate_discount

def test_calculate_discount_normal():
    assert calculate_discount(100, 20) == 80.0
    assert calculate_discount(50, 10) == 45.0

def test_calculate_discount_edge_cases():
    assert calculate_discount(100, 0) == 100.0
    assert calculate_discount(100, 100) == 0.0

def test_calculate_discount_invalid_input():
    with pytest.raises(ValueError):
        calculate_discount(100, -10)
    
    with pytest.raises(ValueError):
        calculate_discount(100, 101)

def test_calculate_discount_zero_price():
    assert calculate_discount(0, 50) == 0.0
```

## Advanced Examples

### 4. Code Refactoring

**Example: Refactor legacy code**

```python
from agents.programming.refactoring import RefactoringAgent

agent = RefactoringAgent(model="gpt-4")

legacy_code = """
def getData(x):
    d = []
    for i in range(len(x)):
        if x[i]['status'] == 'active':
            d.append(x[i])
    return d
"""

refactored = agent.refactor(
    code=legacy_code,
    improvements=["naming", "pythonic", "type-hints"]
)
print(refactored)
```

### 5. Documentation Generation

**Example: Generate comprehensive docs**

```python
from agents.programming.doc_generator import DocGenerator

generator = DocGenerator(model="gpt-4")

code = """
class DataProcessor:
    def __init__(self, config):
        self.config = config
    
    def process(self, data):
        cleaned = self._clean(data)
        return self._transform(cleaned)
    
    def _clean(self, data):
        return [x for x in data if x is not None]
    
    def _transform(self, data):
        return [x * 2 for x in data]
"""

docs = generator.generate_docs(code, style="google")
print(docs)
```

## Integration Examples

### 6. CI/CD Integration

**Example: Automated code review in CI**

```yaml
# .github/workflows/code-review.yml
name: AI Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run AI Code Review
        run: |
          python scripts/ci_code_review.py \
            --pr-number ${{ github.event.pull_request.number }}
```

### 7. IDE Integration

**Example: VS Code extension integration**

```json
{
  "mimosa-flytrap.enableAutoComplete": true,
  "mimosa-flytrap.model": "gpt-4",
  "mimosa-flytrap.temperature": 0.2
}
```

## Batch Processing

### 8. Process Multiple Files

```python
from agents.programming.batch_processor import BatchProcessor

processor = BatchProcessor()

files = [
    "src/module1.py",
    "src/module2.py",
    "src/module3.py"
]

results = processor.process_batch(
    files=files,
    operation="review",
    parallel=True
)

for file, result in results.items():
    print(f"{file}: {result.summary}")
```

## Running Examples

To run these examples:

```bash
# Set up environment
export OPENAI_API_KEY=your_key

# Run single example
python examples/programming/01_code_generation.py

# Run all examples
python examples/programming/run_all.py
```

## Configuration

Examples use the configuration from `docs/configuration/programming/`.

## Next Steps

- Try modifying examples for your use case
- Explore agent parameters
- Check performance tuning options
- Review best practices documentation
