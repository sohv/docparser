from docling.document_converter import DocumentConverter

source = "images/college id.pdf"
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())
