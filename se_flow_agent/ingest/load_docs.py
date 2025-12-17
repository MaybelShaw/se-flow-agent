from pdfplumber import open as pdf_open
import ebooklib
from ebooklib import epub

def load_pdf(file_path):
    """Load and extract text from a PDF file."""
    all_text = []
    with pdf_open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    return "\n".join(all_text)

def load_epub(file_path):
    """Load and extract text from an EPUB file."""
    book = epub.read_epub(file_path)
    all_text = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            all_text.append(item.get_content().decode('utf-8'))
    return "\n".join(all_text)


if __name__ == "__main__":
    pdf_path = "/Users/bobo/Developer/se-flow-agent/data/books/AppendixA/Curriculum Guidelines for Graduate Degree Programs in Software Engineering.pdf"  # Replace with your PDF file path
    content = load_pdf(pdf_path)
    print(content)

    epub_path = "/Users/bobo/Developer/se-flow-agent/data/books/Chapter5/Cloud Reliability Engineering_ Technologies and Tools.epub"  # Replace with your EPUB file path
    content = load_epub(epub_path)
    print(content)  # Print the first 1000 characters of the content