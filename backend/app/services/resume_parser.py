from pdfminer.high_level import extract_text
from fastapi import UploadFile


def extract_text_from_pdf(file: UploadFile) -> str:
    
    # Extract text from a pdf.
    text = extract_text(file.file)
    # Close the file after reading
    file.file.close()
    # Return the extracted text
    if not text:
        return "No text found in the PDF file."
    text = text.strip()
    if not text:
        return "The PDF file is empty or contains no readable text."
    # Return the extracted text
    return text