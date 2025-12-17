from nltk.tokenize import sent_tokenize

def chunk_by_paragraphs(text):
    """
    Splits the input text into chunks based on paragraphs.

    Args:
        text (str): The input text to be chunked.

    Returns:
        List[str]: A list of text chunks, each representing a paragraph.
    """
    paragraphs = text.split('\n')  # Assuming paragraphs are separated by double newlines
    return [para.strip() for para in paragraphs if para.strip()]

def chunk_by_sentences(text):
    return sent_tokenize(text)

if __name__ == "__main__":
    from load_docs import load_pdf, load_epub
    from clean_text import clean_text

    pdf_path = "/Users/bobo/Developer/se-flow-agent/data/books/AppendixA/Curriculum Guidelines for Graduate Degree Programs in Software Engineering.pdf"  # Replace with your PDF file path
    content = load_pdf(pdf_path)
    cleaned_content = clean_text(content)
    chunks = chunk_by_paragraphs(cleaned_content)
    print(len(chunks), "paragraph chunks from PDF." )
    # for i, chunk in enumerate(chunks):
    #     print(f"Chunk {i+1}:\n{chunk}\n")

    # text = """This is the first sentence. Here is the second sentence! And this is the third one? Yes, indeed."""
    # sentence_chunks = chunk_by_sentences(text)
    # print(len(sentence_chunks), "sentence chunks from sample text.")