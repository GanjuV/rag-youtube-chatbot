# 🎬 RAG YouTube Chatbot

Ask any question about a YouTube video and get accurate, grounded answers.

Built with **LangChain**, **HuggingFace**, and **FAISS** — fully open-source, no OpenAI needed.

## How It Works

1. **Fetch** — Downloads the YouTube transcript via `youtube-transcript-api`
2. **Split** — Chunks the text into overlapping 1,000-char segments
3. **Embed** — Converts chunks to semantic vectors using `all-MiniLM-L6-v2`
4. **Store** — Indexes vectors in FAISS for fast similarity search
5. **Retrieve** — Finds the top-4 most relevant chunks for your question
6. **Generate** — An LLM answers using only those chunks (no hallucination)

## Quickdemo
Use my google colab [link](https://colab.research.google.com/drive/1U42agBz71F9vGsaTATB4tLpN35e-SObZ?usp=sharing)

## Quickstart

```bash
git clone https://github.com/your-username/rag-youtube-chatbot
cd rag-youtube-chatbot

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies from requirements.txt
uv pip install -r requirements.txt

# Create environment file and add your HuggingFace token
cp .env.example .env
# Edit .env and set a valid token:
# HUGGINGFACEHUB_API_TOKEN=hf_your_valid_token_here
# A placeholder token will cause a 401 Unauthorized error.

# Run the CLI chatbot
uv run python -m app.cli --video_id kyQ0CRkYhy4

# Run the API server
uv run uvicorn app.api:app --reload --port 8000
```

## API Usage

Start the FastAPI server first:

```bash
uv run uvicorn app.api:app --reload --port 8000
```

### Ingest a video

```bash
curl -X POST http://localhost:8000/ingest \
     -H "Content-Type: application/json" \
     -d '{"video_id": "kyQ0CRkYhy4"}'
```

### Ask a question

```bash
curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the main strategy explained in the video?"}'
```

### Health check

```bash
curl http://localhost:8000/health
```

## Get a Free HuggingFace Token

1. Sign up at https://huggingface.co
2. Go to Settings → Access Tokens → New Token
3. Copy it into your `.env` file

## Stack

| Component  | Tool                                     |
| ---------- | ---------------------------------------- |
| Transcript | youtube-transcript-api                   |
| Splitting  | LangChain RecursiveCharacterTextSplitter |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2   |
| Vector DB  | FAISS (CPU)                              |
| LLM        | GLM-5.1 via HuggingFace Inference API    |
| Framework  | LangChain                                |

## License

MIT
