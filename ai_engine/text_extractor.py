import PyPDF2
import pytesseract
from PIL import Image

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join(p.extract_text() for p in reader.pages)
    return pytesseract.image_to_string(Image.open(file))
