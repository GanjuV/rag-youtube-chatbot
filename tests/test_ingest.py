"""Tests for transcript ingestion and splitting."""

import pytest
from unittest.mock import patch, MagicMock
from src.ingest import fetch_transcript, split_transcript


def test_split_transcript_returns_chunks():
    sample = "This is a test transcript. " * 100
    chunks = split_transcript(sample)
    assert len(chunks) > 0
    assert all(hasattr(c, "page_content") for c in chunks)


def test_split_transcript_chunk_size():
    sample = "word " * 500
    chunks = split_transcript(sample)
    for chunk in chunks:
        assert len(chunk.page_content) <= 1200  # chunk_size + some tolerance


@patch("src.ingest.YouTubeTranscriptApi")
def test_fetch_transcript_success(mock_api_class):
    mock_api = MagicMock()
    mock_api_class.return_value = mock_api
    mock_api.fetch.return_value = [
        MagicMock(text="Hello "),
        MagicMock(text="World")
    ]
    result = fetch_transcript("test_id")
    assert result == "Hello  World"
