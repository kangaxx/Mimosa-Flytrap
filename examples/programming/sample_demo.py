"""
Sample usage of the code generator agent.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.programming.sample_generator import SampleCodeGenerator


def main():
    """Demonstrate basic usage of the code generator."""
    
    print("=" * 60)
    print("Mimosa-Flytrap Sample Agent Demo")
    print("=" * 60)
    print()
    
    # Initialize the agent
    print("1. Initializing code generator...")
    generator = SampleCodeGenerator(model="gpt-4")
    print("   ✓ Code generator initialized")
    print()
    
    # Generate code
    print("2. Generating code...")
    prompt = "Create a function to calculate fibonacci numbers"
    code = generator.generate(prompt)
    
    print(f"   Prompt: {prompt}")
    print(f"   Generated code:")
    print()
    print(code)
    print()
    
    print("=" * 60)
    print("Demo completed!")
    print()
    print("Next steps:")
    print("  - Explore more examples in examples/programming/")
    print("  - Read the documentation in docs/")
    print("  - Create your own agents using templates/")
    print("=" * 60)


if __name__ == '__main__':
    main()
