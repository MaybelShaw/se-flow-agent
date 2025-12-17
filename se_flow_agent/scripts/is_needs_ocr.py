import os
import regex as re
from pdfplumber import open as pdf_open

def scan_pdf(file_path):
    # 递归扫描PDF文件
    os_walk = os.walk(file_path)
    pdf_files = []
    for root, dirs, files in os_walk:
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def needs_ocr(file_path):
    # 简单判断PDF是否需要OCR（例如，检查是否有可提取的文本）
    with pdf_open(file_path) as pdf:
        texts = []
        for page in pdf.pages:
            text = page.extract_text()
            texts.append(text)
        if len(texts)<2000:
            return True
    return False

if __name__ == "__main__":
    print("Scanning PDF files...")
    pdf_directory = "/Users/bobo/Developer/se-flow-agent/data/books"
    pdf_files = scan_pdf(pdf_directory)
    count = 0
    for pdf_file in pdf_files:
        if needs_ocr(pdf_file):
            print(f"OCR needed for: {pdf_file}")
            count += 1
    print(f"Total PDF files needing OCR: {count}")
    print(count / len(pdf_files))