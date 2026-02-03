# Document Processing Agents

This directory contains AI agents for document analysis, transformation, and generation.

## Available Agents

### Document Extraction
- **PDF extractors**: Extract text, tables, and metadata from PDFs
- **OCR agents**: Extract text from scanned documents
- **Table extractors**: Parse and structure tabular data
- **Metadata extractors**: Extract document properties and metadata

### Document Transformation
- **Format converters**: Convert between document formats (PDF, DOCX, MD, etc.)
- **Summarizers**: Generate document summaries
- **Translators**: Translate documents between languages
- **Content rewriters**: Rephrase and restructure content

### Document Generation
- **Report generators**: Create formatted reports from data
- **Template fillers**: Populate document templates
- **Document mergers**: Combine multiple documents
- **Citation managers**: Generate and format citations

### Document Analysis
- **Sentiment analyzers**: Analyze document sentiment and tone
- **Entity extractors**: Identify and extract named entities
- **Topic modelers**: Identify main topics and themes
- **Similarity comparators**: Compare document similarity

### Content Management
- **Indexers**: Create searchable document indexes
- **Classifiers**: Categorize documents automatically
- **Semantic search**: Search documents by meaning
- **Version trackers**: Track document changes

## Usage

Each agent includes:
- Supported document formats
- Processing capabilities
- Configuration parameters
- Performance considerations
- Error handling

## Examples

See `examples/document-processing/` for demonstrations of:
- Basic document processing workflows
- Batch processing examples
- Integration with storage systems
- Advanced use cases

## Configuration

Configuration templates are available in `docs/configuration/document-processing/`.

## Dependencies

Common dependencies for document processing agents:
- PDF processing: PyPDF2, pdfplumber, PyMuPDF
- OCR: Tesseract, EasyOCR
- NLP: spaCy, NLTK, transformers
- Format conversion: pandoc, python-docx

## Contributing

When adding document processing agents:
1. Specify supported formats
2. Include sample input/output files
3. Document performance characteristics
4. Provide error handling examples
5. Update this README
