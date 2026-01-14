# PDF OCR API

A FastAPI-based REST API for extracting text and images from PDF files using Tesseract OCR. The API accepts PDF uploads and returns extracted text along with base64-encoded images for each page.

## Features

- 📄 Upload PDF files via REST API
- 🖼️ Extract images from each page
- 📝 OCR text extraction using Tesseract

## Prerequisites

- Docker and Docker Compose installed on your system
- Or Python 3.11+ with Tesseract OCR and Poppler installed locally

## Quick Start with Docker

### 1. Build and run the container

```bash
docker-compose up --build
```

### 2. Access the API

### Upload PDF and Extract Text

**Endpoint:** `POST /extract-pdf`

**Parameters:**
- `file`: PDF file (required)
- `lang`: OCR language code (optional, default: 'eng')

**Example using cURL:**

```bash
curl -X POST "http://localhost:8000/extract-pdf" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-document.pdf" \
  -F "lang=eng"
```

**Example using Python:**

```python
import requests

url = "http://localhost:8000/extract-pdf"
files = {"file": open("your-document.pdf", "rb")}
params = {"lang": "eng"}

response = requests.post(url, files=files, params=params)
result = response.json()

print(f"Total pages: {result['total_pages']}")
for page in result['pages']:
    print(f"\nPage {page['page_number']}:")
    print(f"Text: {page['text'][:100]}...")  # First 100 chars
    # page['image'] contains base64 encoded PNG
```

**Example using JavaScript/Node.js:**

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('your-document.pdf'));

axios.post('http://localhost:8000/extract-pdf?lang=eng', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log('Total pages:', response.data.total_pages);
  response.data.pages.forEach(page => {
    console.log(`\nPage ${page.page_number}:`);
    console.log('Text:', page.text.substring(0, 100));
  });
})
.catch(error => console.error(error));
```

### Response Format

```json
{
  "filename": "document.pdf",
  "total_pages": 2,
  "language": "eng",
  "pages": [
    {
      "page_number": 1,
      "text": "Extracted text from page 1...",
      "image": "base64_encoded_image_string..."
    },
    {
      "page_number": 2,
      "text": "Extracted text from page 2...",
      "image": "base64_encoded_image_string..."
    }
  ]
}
```

## Supported Languages

The OCR supports multiple languages. Common language codes:

- `eng` - English