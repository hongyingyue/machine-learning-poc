import fitz


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)
    return text
