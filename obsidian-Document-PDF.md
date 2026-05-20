# Document & PDF

Word, Excel, PowerPoint, PDF, and document automation skills.

## Microsoft Office
| Skill | Description | Linked Skills |
|-------|-------------|---------------|
| [[docx-manipulation]] | Create/edit Word documents (python-docx) | [[docx]], [[office-mcp]] |
| [[docx]] | Word document operations | [[docx-manipulation]], [[pdf-to-docx]] |
| [[xlsx-manipulation]] | Create/edit Excel spreadsheets (openpyxl) | [[xlsx]], [[office-mcp]] |
| [[xlsx]] | Excel spreadsheet operations | [[xlsx-manipulation]], [[sheets-automation]] |
| [[pptx-manipulation]] | PowerPoint manipulation | [[pptx]], [[html-to-ppt]], [[simple-deck]] |
| [[pptx]] | PowerPoint operations | [[pptx-manipulation]], [[ppt-visual]] |
| [[office-mcp]] | MCP server for Office operations | [[docx]], [[xlsx]], [[pptx]], [[pdf]] |

## PDF Operations
| Skill | Description | Linked Skills |
|-------|-------------|---------------|
| [[pdf-extraction]] | Extract text, tables, metadata (pdfplumber) | [[pdf-ocr-extraction]], [[smart-ocr]] |
| [[pdf-compress]] | Reduce PDF file size | [[pdf-merge-split]] |
| [[pdf-converter]] | Convert PDF to/from other formats | [[pdf-to-docx]], [[office-to-md]] |
| [[pdf-form-filler]] | Fill out PDF forms programmatically | [[pdf-extraction]] |
| [[pdf-merge-split]] | Combine/split PDFs | [[pdf-compress]] |
| [[pdf-ocr-extraction]] | OCR for scanned PDFs | [[pdf-extraction]], [[smart-ocr]] |
| [[pdf-to-docx]] | Convert PDF to Word | [[docx-manipulation]], [[pdf-converter]] |
| [[pdf-watermark]] | Add watermarks, page numbers | [[pdf-merge-split]] |

## Document Conversion
| Skill | Description | Linked Skills |
|-------|-------------|---------------|
| [[office-to-md]] | Convert Office files to Markdown | [[docx-manipulation]], [[md-slides]] |
| [[html-to-ppt]] | Convert HTML/Markdown to PowerPoint (Marp) | [[pptx-manipulation]], [[md-slides]] |
| [[doc-pipeline]] | Chain document operations | [[doc-parser]], [[template-engine]] |
| [[doc-parser]] | Parse document content | [[doc-pipeline]], [[table-extractor]] |
| [[batch-convert]] | Batch document format conversion | [[office-to-md]], [[pdf-converter]] |

## Templates & Forms
| Skill | Description | Linked Skills |
|-------|-------------|---------------|
| [[template-engine]] | Mail merge for any format | [[docx-manipulation]], [[xlsx-manipulation]] |
| [[invoice-template]] | Professional PDF invoices | [[invoice]], [[invoice-automation]] |
| [[contract-template]] | Contract document templates | [[contract-review]] |
| [[form-builder]] | Interactive document forms (docassemble) | [[pdf-form-filler]] |

## OCR & Extraction
| Skill | Description | Linked Skills |
|-------|-------------|---------------|
| [[smart-ocr]] | Advanced OCR extraction | [[pdf-ocr-extraction]], [[pdf-extraction]] |
| [[table-extractor]] | Extract tables from documents | [[doc-parser]], [[pdf-extraction]] |
| [[data-extractor]] | Structured data extraction | [[pdf-extraction]], [[doc-parser]] |

---

## Related Categories

- [[Productivity]] - For document automation workflows
- [[Marketing & Ads]] - For ad copy documents
- [[Communication]] - For email/templates