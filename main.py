"""
FastAPI application for PDF OCR processing.
Accepts PDF uploads and returns extracted text with page images.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import base64
import io
import os
import tempfile
import shutil
from pathlib import Path

app = FastAPI(
    title="PDF OCR API",
    description="Upload PDF files and get extracted text with page images",
    version="1.0.0"
)


def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')


def process_pdf(pdf_path: str, lang: str = 'eng') -> List[Dict]:
    """
    Process PDF file and extract text with images from each page.
    
    Args:
        pdf_path: Path to the PDF file
        lang: OCR language (default: 'eng')
    
    Returns:
        List of dictionaries containing page number, extracted text, and base64 image
    """
    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=300)
    
    results = []
    
    for i, image in enumerate(images, 1):
        # Extract text using OCR
        text = pytesseract.image_to_string(image, lang=lang)
        
        # Convert image to base64
        image_base64 = image_to_base64(image)
        
        results.append({
            "page_number": i,
            "text": text.strip(),
            "image": image_base64
        })
    
    return results


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "PDF OCR API",
        "endpoints": {
            "/docs": "API documentation",
            "/extract-pdf": "POST endpoint to upload PDF and extract text with images"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/extract-pdf")
async def extract_pdf(
    file: UploadFile = File(...),
    lang: str = 'eng'
):
    """
    Extract text and images from uploaded PDF file.
    
    Args:
        file: PDF file to process
        lang: OCR language code (default: 'eng', can use multiple like 'eng+urd+ara')
    
    Returns:
        JSON with extracted text and base64 encoded images for each page
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Create temporary directory for processing
    temp_dir = tempfile.mkdtemp()
    temp_pdf_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save uploaded file temporarily
        with open(temp_pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the PDF
        results = process_pdf(temp_pdf_path, lang=lang)
        
        return JSONResponse(content={
            "filename": file.filename,
            "total_pages": len(results),
            "language": lang,
            "pages": results
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        # Cleanup temporary files
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
