"""
LangChain AI Agent Example Script

This script demonstrates how to create and run a simple AI agent using LangChain
with support for both OpenAI GPT-3.5 and local Ollama models.

Usage:
    python run_langchain_agent.py [--model gpt|ollama] [--prompt "Your question"]
"""

import os
import sys
import argparse
from typing import Optional

try:
    from dotenv import load_dotenv
    from langchain_openai import ChatOpenAI
    from langchain_community.llms import Ollama
    from langchain.prompts import ChatPromptTemplate, PromptTemplate
    from langchain.chains import LLMChain
except ImportError as e:
    print(f"Error: Required package not found: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


class LangChainAgent:
    """A simple LangChain agent that can use either GPT or Ollama models."""
    
    def __init__(self, model_type: str = "gpt"):
        """
        Initialize the agent with specified model type.
        
        Args:
            model_type: Either "gpt" for OpenAI GPT-3.5 or "ollama" for local Ollama
        """
        # Load environment variables
        load_dotenv()
        
        self.model_type = model_type
        self.llm = self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the appropriate LLM model."""
        if self.model_type == "gpt":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or not api_key.startswith("sk-"):
                raise ValueError(
                    "OpenAI API key not found or invalid. "
                    "Please set OPENAI_API_KEY in your .env file"
                )
            
            model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            temperature = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
            
            print(f"✓ Initializing OpenAI model: {model_name}")
            return ChatOpenAI(
                model=model_name,
                temperature=temperature,
                api_key=api_key
            )
            
        elif self.model_type == "ollama":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model_name = os.getenv("OLLAMA_MODEL", "llama2")
            
            print(f"✓ Initializing Ollama model: {model_name}")
            print(f"  Base URL: {base_url}")
            
            return Ollama(
                model=model_name,
                base_url=base_url
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def run_simple_query(self, question: str) -> str:
        """
        Run a simple query against the model.
        
        Args:
            question: The question to ask the model
            
        Returns:
            The model's response
        """
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}\n")
        
        if self.model_type == "gpt":
            prompt = ChatPromptTemplate.from_template(
                "You are a helpful AI assistant. Answer the following question concisely:\n\n{question}"
            )
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = chain.run(question=question)
        else:
            prompt = PromptTemplate.from_template(
                "You are a helpful AI assistant. Answer the following question concisely:\n\n{question}"
            )
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = chain.run(question=question)
        
        return response
    
    def run_conversation(self):
        """Run an interactive conversation loop."""
        print(f"\n{'='*60}")
        print(f"Interactive LangChain Agent ({self.model_type.upper()})")
        print(f"{'='*60}")
        print("Type 'quit', 'exit', or 'q' to exit")
        print(f"{'='*60}\n")
        
        while True:
            try:
                question = input("You: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\nGoodbye!")
                    break
                
                if not question:
                    continue
                
                print(f"\n{self.model_type.upper()}: ", end="", flush=True)
                response = self.run_simple_query(question)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                continue


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Run a LangChain AI agent with GPT or Ollama"
    )
    parser.add_argument(
        "--model",
        choices=["gpt", "ollama"],
        default="gpt",
        help="Choose the model type: gpt (OpenAI GPT-3.5) or ollama (local)"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Single prompt to run (if not provided, starts interactive mode)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Force interactive mode"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize the agent
        agent = LangChainAgent(model_type=args.model)
        
        if args.prompt and not args.interactive:
            # Single query mode
            response = agent.run_simple_query(args.prompt)
            print(f"\nResponse:\n{response}\n")
        else:
            # Interactive mode
            agent.run_conversation()
            
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
