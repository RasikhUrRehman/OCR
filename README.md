# PDF OCR API

A FastAPI-based REST API for extracting text and images from PDF files using Tesseract OCR. The API accepts PDF uploads and returns extracted text along with base64-encoded images for each page.

## Features

- 📄 Upload PDF files via REST API
- 🖼️ Extract images from each page
- 📝 OCR text extraction using Tesseract
- 🐳 Fully containerized with Docker
- 🚀 Fast and easy to deploy
- 📊 Automatic API documentation with Swagger UI

## Prerequisites

- Docker and Docker Compose installed on your system
- Or Python 3.11+ with Tesseract OCR and Poppler installed locally

## Quick Start with Docker

### 1. Build and run the container

```bash
docker-compose up --build
```

### 2. Access the API

The API will be available at: `http://localhost:8000`

- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative Documentation (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## API Usage

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
- `ara` - Arabic
- `urd` - Urdu
- `fra` - French
- `deu` - German
- `spa` - Spanish
- `chi_sim` - Simplified Chinese

You can use multiple languages: `eng+urd+ara`

To add more languages to the Docker image, modify the Dockerfile:

```dockerfile
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-ara \
    tesseract-ocr-urd \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*
```

## Local Development (Without Docker)

### 1. Install system dependencies

**Windows:**
- Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Install Poppler: Download from https://github.com/oschwartz10612/poppler-windows/releases/

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

**macOS:**
```bash
brew install tesseract poppler
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload
```

## Project Structure

```
.
├── main.py                 # FastAPI application
├── test.ipynb             # Original OCR notebook
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose setup
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Docker Commands

### Build the image
```bash
docker build -t pdf-ocr-api .
```

### Run the container
```bash
docker run -p 8000:8000 pdf-ocr-api
```

### Using Docker Compose
```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs -f
```

## Testing the API

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click on the POST `/extract-pdf` endpoint
3. Click "Try it out"
4. Upload a PDF file
5. Click "Execute"

### Using Postman

1. Create a new POST request to `http://localhost:8000/extract-pdf`
2. Go to Body → form-data
3. Add key `file` with type `File` and select your PDF
4. Optionally add key `lang` with value `eng`
5. Send the request

## Performance Tips

- The API processes PDFs at 300 DPI by default for good quality
- Processing time depends on the number of pages and image quality
- For large PDFs, consider implementing pagination or async processing
- Base64 encoding increases the response size significantly

## Troubleshooting

### Error: "Tesseract not found"
- Ensure Tesseract is installed in the Docker container
- For local development, verify Tesseract is in your PATH

### Error: "poppler not found"
- Ensure poppler-utils is installed
- For Windows, set the poppler_path parameter

### Large response sizes
- Base64 encoding images increases size by ~33%
- Consider implementing pagination for large PDFs
- Or return image URLs instead of base64 data

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Built with ❤️ using FastAPI, Tesseract OCR, and Docker
