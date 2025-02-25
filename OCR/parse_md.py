from docling.document_converter import DocumentConverter

source = "images/college id.pdf"  # document per local path or URL
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())
# output: ## Docling Technical Report [...]"