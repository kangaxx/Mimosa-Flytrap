# Mimosa-Flytrap Setup

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mimosa-flytrap",
    version="1.0.0",
    author="kangaxx",
    description="A curated repository of AI Agent scripts and documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kangaxx/Mimosa-Flytrap",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "programming": [
            "openai>=1.0.0",
            "anthropic>=0.7.0",
        ],
        "document-processing": [
            "pypdf2>=3.0.0",
            "python-docx>=0.8.11",
            "pdfplumber>=0.9.0",
        ],
        "image-processing": [
            "pillow>=10.0.0",
            "opencv-python>=4.8.0",
        ],
        "all": [
            "openai>=1.0.0",
            "anthropic>=0.7.0",
            "pypdf2>=3.0.0",
            "python-docx>=0.8.11",
            "pdfplumber>=0.9.0",
            "pillow>=10.0.0",
            "opencv-python>=4.8.0",
        ],
    },
)
