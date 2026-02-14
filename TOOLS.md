## DDGS API (localhost:8000)
FastAPI wrapper for DDGS. Use `curl` for localhost (not web_fetch).

### Endpoints
- `GET /search/text` - Text search
- `GET /search/news` - News search
- `GET /search/images` - Image search

### Quick example
```bash
curl -s 'http://localhost:8000/search/text?query=anime&region=us-en&safesearch=moderate&max_results=10' -H 'accept: application/json'
```

### Scripts
- `search_ddgs.sh` - Text search wrapper (URL-encodes, formats with jq)
- `skills/image-search/scripts/search_images.sh` - Image search + download to `/tmp/clawko-images/`
