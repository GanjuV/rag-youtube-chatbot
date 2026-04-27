"""FAISS vector store creation and retrieval."""

import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings.huggingface_endpoint import HuggingFaceEndpointEmbeddings
from src.config import EMBEDDING_MODEL, TOP_K, FAISS_INDEX_PATH


def build_vector_store(chunks: list) -> FAISS:
    """Create a FAISS vector store from document chunks."""
    embedding = HuggingFaceEndpointEmbeddings(model=EMBEDDING_MODEL)
    return FAISS.from_documents(chunks, embedding)


def save_vector_store(vector_store: FAISS, path: str = FAISS_INDEX_PATH):
    """Save the FAISS vector store to disk."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    vector_store.save_local(path)


def load_vector_store(path: str = FAISS_INDEX_PATH) -> FAISS:
    """Load a FAISS vector store from disk."""
    embedding = HuggingFaceEndpointEmbeddings(model=EMBEDDING_MODEL)
    return FAISS.load_local(path, embedding, allow_dangerous_deserialization=True)


def get_retriever(vector_store: FAISS):
    """Return a similarity retriever with top-K results."""
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K}
    )
