from se_flow_agent.retriever.vector_store import ChromaVectorStore
from se_flow_agent.retriever.embedding import SentenceTransformerEmbedder
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from langchain.tools import tool

class RetrieverInterface(ABC):
    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict[str, any]]:
        pass

class SimpleRetriever(RetrieverInterface):
    def __init__(self, vector_store: ChromaVectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, any]]:
        query_embedding = SentenceTransformerEmbedder().embed_texts([query])[0]
        results = self.vector_store.query(embedding=query_embedding, top_k=top_k)
        return results

@tool
def retrieve_tool(query: str, top_k: int = 5) -> List[Dict[str, any]]:
    """Retrieve relevant documents from the vector store."""
    vector_store = ChromaVectorStore(collection_name="test_collection")
    retriever = SimpleRetriever(vector_store=vector_store)
    return retriever.retrieve(query=query, top_k=top_k)

if __name__ == "__main__":
    vector_store = ChromaVectorStore(collection_name="test_collection")
    retriever = SimpleRetriever(vector_store=vector_store)
    query = "Sample query text"
    results = retriever.retrieve(query=query, top_k=3)
    for result in results:
        print(result)