from sentence_transformers import SentenceTransformer

def embed_texts(texts, model_name="all-MiniLM-L6-v2"):
    """
    使用 SentenceTransformer 对文本进行嵌入。

    参数:
        texts (List[str]): 需要嵌入的文本列表。
        model_name (str): 使用的预训练模型名称。
    返回:
        List[List[float]]: 嵌入向量列表。
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, convert_to_tensor=False)
    return embeddings

if __name__ == "__main__":
    sample_texts = [
        "This is a sample sentence.",
        "Another example of text to embed."
    ]
    embeddings = embed_texts(sample_texts)
    for i, emb in enumerate(embeddings):
        print(f"Text: {sample_texts[i]}\nEmbedding: {emb}\n")
