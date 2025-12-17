import os
import uuid
import chromadb
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class VectorStoreInterface(ABC):
    @abstractmethod
    def add(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
        pass

    @abstractmethod
    def query(
        self,
        embedding: List[float],
        top_k: int = 5,
        where: Optional[dict] = None,
    ) -> List[Dict[str, any]]:
        pass

    @abstractmethod
    def delete(
        self,
        ids: Optional[List[str]] = None,
        where: Optional[dict] = None,
    ) -> None:
        pass

    @abstractmethod
    def update(
        self,
        ids: List[str],
        documents: Optional[List[str]] = None,
        embeddings: Optional[List[List[float]]] = None,
        metadatas: Optional[List[dict]] = None,
    ) -> None:
        pass

    @abstractmethod
    def get_by_id(
        self,
        id: str,
    ) -> Optional[Dict[str, any]]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def peek(self, n: int = 5) -> List[Dict[str, any]]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass


class ChromaVectorStore(VectorStoreInterface):
    def __init__(
        self,
        collection_name: str = "default_collection",
        persist_directory: Optional[str] = None,
    ):
        if persist_directory is None:
            root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            persist_directory = os.path.join(root_path, "data", "chroma_db")
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
        batch_size = 500
        if len(documents) != len(embeddings):
            raise ValueError("Documents and embeddings must have the same length")
        if metadatas is not None and len(metadatas) != len(documents):
            raise ValueError("Metadatas length must match documents length")
        if ids is not None and len(ids) != len(documents):
            raise ValueError("IDs length must match documents length")

        # Generate UUIDs when ids are not provided to satisfy Chroma's non-null id requirement
        _metadatas = metadatas if metadatas is not None else [None] * len(documents)
        _ids = ids if ids is not None else [str(uuid.uuid4()) for _ in documents]
        for i in range(0, len(documents), batch_size):
            self.collection.add(
                documents=documents[i : i + batch_size],
                embeddings=embeddings[i : i + batch_size],
                metadatas=_metadatas[i : i + batch_size],
                ids=_ids[i : i + batch_size],
            )

    def query(
        self, embedding: List[float], top_k: int = 5, where: Optional[dict] = None
    ) -> List[Dict[str, any]]:
        results = self.collection.query(
            query_embeddings=[embedding], n_results=top_k, where=where
        )
        # Chroma返回结构：{'ids': [[id1, id2,...]], 'documents': [[doc1, doc2,...]], ...}
        items = []
        # 遍历第一个（也是唯一一个）查询结果批次
        for i in range(len(results["ids"][0])):
            item = {
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": (
                    results["metadatas"][0][i] if results["metadatas"] else None
                ),
            }
            items.append(item)
        return items

    def delete(
        self,
        ids: Optional[List[str]] = None,
        where: Optional[dict] = None,
    ) -> None:
        if ids:
            self.collection.delete(ids=ids)
        elif where:
            self.collection.delete(where=where)
        else:
            raise ValueError("Either 'ids' or 'where' must be provided for deletion.")

    def update(
        self,
        ids: List[str],
        documents: Optional[List[str]] = None,
        embeddings: Optional[List[List[float]]] = None,
        metadatas: Optional[List[dict]] = None,
    ) -> None:
        # 前置校验逻辑...
        # 准备批量更新数据
        if documents is not None and len(documents) != len(ids):
            raise ValueError("Number of documents must match number of ids")
        if embeddings is not None and len(embeddings) != len(ids):
            raise ValueError("Number of embeddings must match number of ids")
        if metadatas is not None and len(metadatas) != len(ids):
            raise ValueError("Number of metadatas must match number of ids")
        update_kwargs = {"ids": ids}
        if documents:
            update_kwargs["documents"] = documents
        if embeddings:
            update_kwargs["embeddings"] = embeddings
        if metadatas:
            update_kwargs["metadatas"] = metadatas
        # 单次调用
        self.collection.update(**update_kwargs)

    def get_by_id(self, id: str) -> Optional[Dict[str, any]]:
        results = self.collection.get(ids=[id])
        if results["ids"]:
            return {
                "id": results["ids"][0],
                "document": results["documents"][0],
                "embedding": (
                    results["embeddings"][0] if results.get("embeddings") else None
                ),  # 关键修正
                "metadata": (
                    results["metadatas"][0] if results.get("metadatas") else None
                ),  # 关键修正
            }
        return None

    def count(self) -> int:
        return self.collection.count()

    def peek(self, n: int = 5) -> List[Dict[str, any]]:
        results = self.collection.get(limit=n)
        items = []
        for i in range(len(results["ids"])):
            items.append(
                {
                    "id": results["ids"][i],
                    "document": results["documents"][i],
                    "metadata": (
                        results["metadatas"][i] if results["metadatas"] else None
                    ),
                    "embedding": (
                        results["embeddings"][i] if results["embeddings"] else None
                    ),
                }
            )
        return items

    def clear(self) -> None:
        # Drop and recreate the collection to remove all entries without requiring filters
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

if __name__ == "__main__":
    vector_store = ChromaVectorStore(collection_name="test_collection")
    print("Vector store initialized.")

    # Add sample data
    documents = ["Hello world", "ChromaDB vector store", "Test document"]
    embeddings = [[0.1] * 384, [0.2] * 384, [0.3] * 384]  # Example embeddings
    vector_store.add(documents, embeddings)
    print("Sample documents added.")

    # Query sample data
    query_embedding = [0.1] * 384
    results = vector_store.query(query_embedding, top_k=2)
    print("Query results:", results)

    # Count documents
    count = vector_store.count()
    print("Total documents in vector store:", count)
    # Peek documents
    peeked = vector_store.peek(n=2)
    print("Peeked documents:", peeked)

    # Clear the collection
    # vector_store.clear()
    # print("Vector store cleared.")
    # count_after_clear = vector_store.count()
    # print("Total documents after clear:", count_after_clear)
