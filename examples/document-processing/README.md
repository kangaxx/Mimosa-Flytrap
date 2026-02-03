# Document Processing Examples

Practical examples for document processing agents.

## Basic Examples

### 1. PDF Text Extraction

```python
from agents.document_processing.pdf_extractor import PDFExtractor

# Initialize the agent
extractor = PDFExtractor()

# Extract text from PDF
text = extractor.extract_text("documents/sample.pdf")
print(text)

# Extract with metadata
result = extractor.extract_with_metadata("documents/sample.pdf")
print(f"Pages: {result['pages']}")
print(f"Author: {result['metadata']['author']}")
print(f"Text: {result['text']}")
```

### 2. Document Summarization

```python
from agents.document_processing.summarizer import DocumentSummarizer

summarizer = DocumentSummarizer(model="gpt-4")

# Read document
with open("documents/report.txt", "r") as f:
    text = f.read()

# Generate summary
summary = summarizer.summarize(
    text=text,
    max_length=200,
    style="bullet-points"
)

print("Summary:")
print(summary)
```

**Output:**
```
Summary:
• Key findings from Q4 2024 revenue analysis
• 15% growth in customer acquisition
• Cloud services remain top revenue driver
• Recommendations for 2025 strategy
• Focus areas: mobile expansion and AI integration
```

### 3. Document Translation

```python
from agents.document_processing.translator import DocumentTranslator

translator = DocumentTranslator(model="gpt-4")

# Translate document
translated = translator.translate(
    source_file="documents/report_en.pdf",
    target_language="Spanish",
    preserve_formatting=True
)

# Save translated document
translated.save("documents/report_es.pdf")
```

### 4. Entity Extraction

```python
from agents.document_processing.entity_extractor import EntityExtractor

extractor = EntityExtractor()

text = """
John Smith, CEO of TechCorp, announced a new partnership 
with Microsoft on January 15, 2024 in San Francisco. The 
deal is valued at $50 million.
"""

entities = extractor.extract(text)

print("Entities found:")
for entity_type, entities_list in entities.items():
    print(f"{entity_type}: {entities_list}")
```

**Output:**
```
Entities found:
PERSON: ['John Smith']
ORGANIZATION: ['TechCorp', 'Microsoft']
DATE: ['January 15, 2024']
LOCATION: ['San Francisco']
MONEY: ['$50 million']
```

## Advanced Examples

### 5. Batch Document Processing

```python
from agents.document_processing.batch_processor import BatchProcessor
import glob

processor = BatchProcessor()

# Process all PDFs in directory
pdf_files = glob.glob("documents/*.pdf")

results = processor.process_batch(
    files=pdf_files,
    operations=[
        "extract_text",
        "summarize",
        "extract_entities"
    ],
    parallel=True,
    max_workers=4
)

# Generate report
for file, result in results.items():
    print(f"\n{file}:")
    print(f"  Summary: {result['summary'][:100]}...")
    print(f"  Entities: {len(result['entities'])} found")
```

### 6. Document Comparison

```python
from agents.document_processing.comparator import DocumentComparator

comparator = DocumentComparator(model="gpt-4")

# Compare two documents
similarity = comparator.compare(
    doc1="documents/version1.pdf",
    doc2="documents/version2.pdf",
    output_changes=True
)

print(f"Similarity: {similarity['score']:.2%}")
print("\nChanges detected:")
for change in similarity['changes']:
    print(f"  - {change['type']}: {change['description']}")
```

### 7. Template-Based Generation

```python
from agents.document_processing.generator import TemplateGenerator

generator = TemplateGenerator()

# Load template
template = generator.load_template("templates/report_template.docx")

# Fill with data
data = {
    "title": "Q4 Financial Report",
    "date": "December 31, 2024",
    "summary": "Strong performance with 20% growth",
    "metrics": [
        {"name": "Revenue", "value": "$10M"},
        {"name": "Profit", "value": "$2M"}
    ]
}

# Generate document
document = generator.generate(template, data)
document.save("output/q4_report.docx")
```

### 8. OCR Processing

```python
from agents.document_processing.ocr import OCRAgent

ocr = OCRAgent(engine="tesseract")

# Process scanned document
text = ocr.extract_text_from_image(
    "scans/invoice.png",
    language="eng",
    preprocessing=True
)

# Extract structured data
invoice_data = ocr.extract_invoice_data(text)

print(f"Invoice #: {invoice_data['number']}")
print(f"Date: {invoice_data['date']}")
print(f"Total: {invoice_data['total']}")
```

## Integration Examples

### 9. Document Pipeline

```python
from agents.document_processing.pipeline import DocumentPipeline

# Create processing pipeline
pipeline = DocumentPipeline([
    ("extract", {"format": "pdf"}),
    ("clean", {"remove_headers": True}),
    ("summarize", {"max_length": 200}),
    ("translate", {"target": "Spanish"}),
    ("save", {"format": "docx"})
])

# Process document through pipeline
result = pipeline.process("input/document.pdf")
print(f"Processed document saved to: {result['output_path']}")
```

### 10. Semantic Search

```python
from agents.document_processing.semantic_search import SemanticSearch

# Initialize search engine
search = SemanticSearch()

# Index documents
search.index_directory("documents/", recursive=True)

# Search by meaning
results = search.search(
    query="financial performance metrics",
    top_k=5
)

for result in results:
    print(f"{result['file']}: {result['score']:.2f}")
    print(f"  Excerpt: {result['excerpt']}\n")
```

## Format Conversion Examples

### 11. Multi-Format Conversion

```python
from agents.document_processing.converter import FormatConverter

converter = FormatConverter()

# PDF to Word
converter.convert("input.pdf", "output.docx")

# Markdown to PDF
converter.convert("README.md", "README.pdf", style="github")

# HTML to DOCX
converter.convert("page.html", "document.docx")
```

## Running Examples

```bash
# Install dependencies
pip install -r agents/document-processing/requirements.txt

# Run single example
python examples/document-processing/01_pdf_extraction.py

# Run all examples
python examples/document-processing/run_all.py

# Process with custom config
python examples/document-processing/process.py \
  --input documents/ \
  --operation summarize \
  --config config/custom.yaml
```

## Sample Documents

Sample documents for testing are available in `examples/document-processing/samples/`:
- `sample.pdf` - Multi-page PDF document
- `invoice.png` - Scanned invoice image
- `report.docx` - Word document
- `article.txt` - Plain text article

## Configuration

Example configurations in `docs/configuration/document-processing/`.

## Next Steps

- Explore different document formats
- Try custom extraction patterns
- Experiment with summarization styles
- Build custom processing pipelines
