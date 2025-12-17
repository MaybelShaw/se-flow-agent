import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pdfplumber import open as pdf_open
import ebooklib
from ebooklib import epub


@dataclass
class Document:
    title: str
    metadata: Dict[str, any] = field(default_factory=dict)
    content: str = field(default_factory=str)

    def update_metadata(self, metadata: Dict[str, any]) -> None:
        self.metadata.update(metadata)


class DocumentLoader:
    def __init__(self):
        pass

    def load_pdf(self, file_path: str) -> Document:
        with pdf_open(file_path) as pdf:
            document = Document(title=os.path.basename(file_path).split(".")[0])
            document.update_metadata(pdf.metadata)
            content = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"
            document.content = content
        return document

    def load_epub(self, file_path: str) -> Document:
        book = epub.read_epub(file_path)
        doc = Document(title=os.path.basename(file_path).split(".")[0])
        doc.update_metadata(book.metadata)
        content = ""
        for item in book.items:
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                content += item.content
        doc.content = content
        return doc


if __name__ == "__main__":
    pdf_path = "/Users/bobo/Developer/se-flow-agent/data/books/Chapter1/An Analysis of the Requirements Traceability Problem.pdf"
    documentLoader = DocumentLoader()
    doc = documentLoader.load_pdf(pdf_path)
    print(doc.title)
    print(doc.metadata)
    print(doc.content[1000:2000])
