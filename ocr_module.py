import cv2
import pytesseract
import pdf2image
import re
import os

import sys

# Set tesseract path based on Operating System
if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def process_document(file_path: str):
    if file_path.lower().endswith(".pdf"):
        
        pages = pdf2image.convert_from_path(file_path)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page)
    else:
        img = cv2.imread(file_path)
        if img is None:
            return ""
        text = pytesseract.image_to_string(img)
    return text

def extract_fields(text: str, doc_type: str):
    extracted_name = ""
    extracted_dob = ""
    extracted_address = ""
    
    # Simple regex-based extraction as a prototype
    dob_match = re.search(r'\b(\d{2}[/-]\d{2}[/-]\d{4})\b', text)
    if dob_match:
        extracted_dob = dob_match.group(1)
        
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        extracted_name = lines[0] # Very naive fallback
        
    return {
        "extractedName": extracted_name,
        "extractedDob": extracted_dob,
        "extractedAddress": text[:100] + "..." if text else "" # Mocking address extraction
    }