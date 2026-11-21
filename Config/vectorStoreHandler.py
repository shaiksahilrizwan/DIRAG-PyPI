from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

try:
    from ..Exceptions.exceptions import VectorStoreSaveError, VectorSearchFail
except ImportError:
    from Exceptions.exceptions import VectorStoreSaveError, VectorSearchFail


class VectorStoreHandler:
    def __init__(
        self,
        embed_model: OllamaEmbeddings,
        collection_name: str,
    ):
        self.embed_model = embed_model
        self.collection_name = collection_name
        store_path = Path.cwd() / "vstore"
        store_path.mkdir(exist_ok=True)
        try:
            self.vector_store = Chroma(
                embedding_function=self.embed_model,
                persist_directory=str(store_path),
                collection_name=collection_name,
            )
        except Exception as exc:
            raise VectorStoreSaveError("Unable to start vector store") from exc

    def save_docs(self, docs):
        try:
            self.vector_store.add_documents(docs)
        except Exception as exc:
            raise VectorStoreSaveError("Unable to save documents") from exc

    def get_docs(self, search_query: str, no_records: int):
        try:
            return self.vector_store.similarity_search(
                query=search_query,
                k=no_records,
            )
        except Exception as exc:
            raise VectorSearchFail("Failed to retrieve relevant information") from exc
