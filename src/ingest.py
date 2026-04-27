"""Fetch YouTube transcripts and split into chunks."""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from langchain_core.documents import Document
from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def fetch_transcript(video_id: str) -> str:
    """Fetch the full transcript for a YouTube video."""
    try:
        ytt = YouTubeTranscriptApi()
        transcript_list = ytt.fetch(video_id)
        return " ".join(chunk.text for chunk in transcript_list)
    except TranscriptsDisabled:
        raise ValueError(f"Transcripts are disabled for video: {video_id}")
    except NoTranscriptFound:
        raise ValueError(f"No transcript found for video: {video_id}")


def split_transcript(transcript: str) -> list[Document]:
    """Split a transcript into overlapping chunks."""
    if not transcript:
        return []

    chunks: list[Document] = []
    start = 0
    length = len(transcript)

    while start < length:
        end = start + CHUNK_SIZE
        chunk_text = transcript[start:end]
        chunks.append(Document(page_content=chunk_text))
        if end >= length:
            break
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks
