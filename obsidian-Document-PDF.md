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
| [[nano-pdf]] | Natural language PDF editing CLI | [[pdf-watermark]], [[pdf-form-filler]] |

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
| [[invoice]] | Printable invoice page | [[invoice-automation]], [[pricing-page]] |
| [[invoice-automation]] | Automate invoice generation & sending | [[invoice-generator]], [[quickbooks-automation]] |
| [[invoice-generator]] | Create professional invoices | [[invoice-organizer]], [[invoice-template]] |
| [[invoice-organizer]] | Organize, categorize & track invoices | [[invoice-generator]], [[expense-tracker]] |
| [[invoice-template]] | Generate PDF invoices from templates | [[invoice-generator]], [[template]] |
| [[expense-report]] | Expense report creation | [[expense-tracker]], [[invoice-organizer]] |
| [[expense-tracker]] | Automate expense tracking & receipt processing | [[invoice-organizer]], [[quickbooks-automation]] |
| [[offer-letter-generator]] | Create formal employment offer letters | [[contract-template]], [[nda-generator]] |
| [[nda-generator]] | Non-disclosure agreement generator | [[contract-template]], [[offer-letter-generator]] |
| [[contract-template]] | Contract template generation | [[docx-manipulation]], [[template]] |

## OCR & Extraction
| Skill | Description | Linked Skills |
|-------|-------------|---------------|
| [[smart-ocr]] | Advanced OCR extraction | [[pdf-ocr-extraction]], [[pdf-extraction]] |
| [[table-extractor]] | Extract tables from documents | [[doc-parser]], [[pdf-extraction]] |
| [[data-extractor]] | Structured data extraction | [[pdf-extraction]], [[doc-parser]] |

## Meeting & Notes
| Skill | Description | Linked Skills |
|-------|-------------|---------------|
| [[meeting-notes]] | Meeting notes automation | [[transcription-automation]], [[calendar-automation]] |
| [[notebooklm]] | Google NotebookLM API access | [[ai-agent-builder]], [[deep-research]] |

---

## Related Categories

- [[Productivity]] - For document automation workflows
- [[Marketing & Ads]] - For ad copy documents
- [[Communication]] - For email/templates