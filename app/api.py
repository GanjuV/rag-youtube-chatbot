"""FastAPI REST API for RAG YouTube Chatbot."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from src.ingest import fetch_transcript, split_transcript
from src.retriever import build_vector_store, save_vector_store, load_vector_store, get_retriever
from src.chain import build_chain
from src.config import FAISS_INDEX_PATH

app = FastAPI(title="RAG YouTube Chatbot API", version="1.0.0")

# In-memory storage for loaded chains (for simplicity)
chains = {}


class IngestRequest(BaseModel):
    video_id: str


class AskRequest(BaseModel):
    question: str


@app.post("/ingest")
def ingest_video(request: IngestRequest):
    """Ingest a YouTube video for Q&A."""
    video_id = request.video_id
    index_path = f"{FAISS_INDEX_PATH}_{video_id}"
    
    try:
        if not os.path.exists(index_path):
            print(f"📥 Fetching transcript for video: {video_id}")
            transcript = fetch_transcript(video_id)
            
            print("✂️  Splitting transcript into chunks...")
            chunks = split_transcript(transcript)
            print(f"   → {len(chunks)} chunks created")
            
            print("🔍 Building vector store...")
            vector_store = build_vector_store(chunks)
            
            print("💾 Saving index...")
            save_vector_store(vector_store, index_path)
        
        # Load and prepare chain
        vector_store = load_vector_store(index_path)
        retriever = get_retriever(vector_store)
        chain = build_chain(retriever)
        chains[video_id] = chain
        
        return {"message": f"Video {video_id} ingested successfully"}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@app.post("/ask")
def ask_question(request: AskRequest):
    """Ask a question about the ingested video."""
    question = request.question
    
    if not chains:
        raise HTTPException(status_code=400, detail="No video ingested yet. Use /ingest first.")
    
    # For simplicity, use the last ingested video
    video_id = list(chains.keys())[-1]
    chain = chains[video_id]
    
    try:
        answer = chain.invoke(question)
        return {"answer": answer, "video_id": video_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "ingested_videos": list(chains.keys())}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)