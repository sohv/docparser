import os
from dotenv import load_dotenv
from mistralai import Mistral, DocumentURLChunk
from mistralai.models import OCRResponse
from pathlib import Path
import json

load_dotenv()

api_key = os.getenv('MISTRAL_API_KEY')

if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env file.")

client = Mistral(api_key=api_key)

pdf_file = Path("./images/college id.pdf")
assert pdf_file.is_file()

uploaded_file = client.files.upload(
    file={
        "file_name": pdf_file.stem,
        "content": pdf_file.read_bytes(),
    },
    purpose="ocr",
)

signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

# Process PDF with OCR
pdf_response = client.ocr.process(
    document=DocumentURLChunk(document_url=signed_url.url),
    model="mistral-ocr-latest",
    include_image_base64=True
)
# Convert response to JSON format
response_dict = json.loads(pdf_response.model_dump_json())

print(json.dumps(response_dict, indent=4)[0:1000])
