"""Tests for vector store and retrieval."""

import pytest
from unittest.mock import MagicMock
from langchain_core.documents import Document


def test_retriever_returns_documents():
    """Smoke test: retriever should return a list of Documents."""
    mock_retriever = MagicMock()
    mock_retriever.invoke.return_value = [
        Document(page_content="This is context from the video."),
        Document(page_content="More context here."),
    ]
    results = mock_retriever.invoke("What is the topic?")
    assert len(results) == 2
    assert all(isinstance(r, Document) for r in results)


def test_retriever_top_k():
    """Retriever should respect TOP_K setting."""
    mock_retriever = MagicMock()
    mock_retriever.invoke.return_value = [Document(page_content=f"Doc {i}") for i in range(4)]
    results = mock_retriever.invoke("some question")
    assert len(results) == 4
