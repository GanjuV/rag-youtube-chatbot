# Examples

## Sample Q&A Sessions

### Example 1: Content Strategy Video

**Video ID:** `kyQ0CRkYhy4` (YouTube content creation strategy)

**Q:** What is the main strategy explained in the video?  
**A:** The video explains a content repurposing strategy where creators should take their best-performing content and transform it into multiple formats across different platforms. This includes turning blog posts into videos, videos into podcasts, and social media posts into newsletters.

**Q:** What did they say about paid ads?  
**A:** I couldn't find that information in the video transcript.

### Example 2: Tech Tutorial Video

**Video ID:** `jX2C3UuFpn4` (Python tutorial)

**Q:** How do you install packages in Python?  
**A:** You can install packages using pip. The command is `pip install package_name`. For example, `pip install requests` installs the requests library.

**Q:** What is a virtual environment?  
**A:** A virtual environment is an isolated Python environment that allows you to install packages for a specific project without affecting the global Python installation. You can create one using `python -m venv myenv` and activate it with `source myenv/bin/activate` on Unix or `myenv\Scripts\activate` on Windows.

## API Usage Examples

### Ingest a Video

```bash
curl -X POST http://localhost:8000/ingest \
     -H "Content-Type: application/json" \
     -d '{"video_id": "kyQ0CRkYhy4"}'
```

### Ask Questions

```bash
curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the main strategy?"}'
```

Response:

```json
{
  "answer": "The video explains a content repurposing strategy...",
  "video_id": "kyQ0CRkYhy4"
}
```

## CLI Usage Examples

### First Run (Ingestion)

```bash
python -m app.cli --video_id kyQ0CRkYhy4
# Downloads transcript, builds index, starts chat
```

### Subsequent Runs

```bash
python -m app.cli --video_id kyQ0CRkYhy4
# Loads existing index, starts chat immediately
```

### Force Re-ingestion

```bash
python -m app.cli --video_id kyQ0CRkYhy4 --reindex
# Rebuilds index even if it exists
```
