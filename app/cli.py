"""Command-line chatbot for RAG YouTube Chatbot."""

import argparse
import os
from huggingface_hub import errors
from src.ingest import fetch_transcript, split_transcript
from src.retriever import build_vector_store, save_vector_store, load_vector_store, get_retriever
from src.chain import build_chain
from src.config import FAISS_INDEX_PATH


def ingest_video(video_id: str, force_reindex: bool = False):
    """Ingest a video: fetch, split, embed, save index."""
    index_path = f"{FAISS_INDEX_PATH}_{video_id}"
    
    if os.path.exists(index_path) and not force_reindex:
        print(f"📁 Index already exists for {video_id}. Use --reindex to rebuild.")
        return load_vector_store(index_path)
    
    print(f"📥 Fetching transcript for video: {video_id}")
    transcript = fetch_transcript(video_id)
    
    print("✂️  Splitting transcript into chunks...")
    chunks = split_transcript(transcript)
    print(f"   → {len(chunks)} chunks created")
    
    print("🔍 Building vector store...")
    vector_store = build_vector_store(chunks)
    
    print("💾 Saving index...")
    save_vector_store(vector_store, index_path)
    
    return vector_store


def chat_loop(chain):
    """Interactive chat loop."""
    print("\n🤖 Chatbot ready! Ask questions about the video (type 'quit' to exit):")
    while True:
        try:
            question = input("\nYou: ").strip()
            if question.lower() in ['quit', 'exit', 'q']:
                break
            if not question:
                continue
                
            print("🤖 Thinking...")
            try:
                answer = chain.invoke(question)
                print(f"Bot: {answer}")
            except errors.HfHubHTTPError as exc:
                if "503" in str(exc):
                    print("Bot: 🚫 HuggingFace service is temporarily unavailable. Please try again in a moment.")
                elif "401" in str(exc) or "Unauthorized" in str(exc):
                    print("Bot: 🚫 HuggingFace authentication failed. Check your token.")
                else:
                    print(f"Bot: 🚫 Error calling HuggingFace API: {exc}")
            
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    
    print("\n👋 Goodbye!")


def main():
    parser = argparse.ArgumentParser(description="RAG YouTube Chatbot CLI")
    parser.add_argument("--video_id", required=True, help="YouTube video ID")
    parser.add_argument("--reindex", action="store_true", help="Force re-ingestion even if index exists")
    args = parser.parse_args()
    
    # Ingest the video
    try:
        vector_store = ingest_video(args.video_id, args.reindex)
    except errors.HfHubHTTPError as exc:
        print("🚫 HuggingFace authentication failed. Check your HUGGINGFACEHUB_API_TOKEN in .env.")
        print(f"Error: {exc}")
        return
    except Exception as exc:
        print(f"🚫 Failed to ingest the video: {exc}")
        return

    retriever = get_retriever(vector_store)
    
    print("⛓️  Assembling RAG chain...")
    chain = build_chain(retriever)
    
    # Start chat
    chat_loop(chain)


if __name__ == "__main__":
    main()