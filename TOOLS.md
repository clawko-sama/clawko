## DDGS API Search Methods (Working ✅)
- Service: localhost:8000 - FastAPI wrapper for DDGS (Dux Distributed Global Search)
- Best Practice: Use curl instead of web_fetch for localhost (direct HTTP access, no MCP mapping)
- Success Results: Successfully searched anime news and love hotels

## Search Endpoints
- GET /search/text  - Text search with query parameters
- GET /search/news  - News search with query parameters  
- POST /search/text - Text search with JSON body
- POST /search/news - News search with JSON body

## Example curl Commands

### Load successful search commands:
curl -X 'GET' 'http://localhost:8000/search/text?query=anime&region=us-en&safesearch=moderate&max_results=10&page=1&backend=auto' -H 'accept: application/json'

#### Love Hotel Search:
curl -s 'http://localhost:8000/search/text?query=love%20hotel%20tokyo&max_results=5&region=us-en'
curl -s 'http://localhost:8000/search/text?query=Hotel%20Secret%20Tokyo&max_results=5&region=us-en'

#### Anime News:
curl -s 'http://localhost:8000/search/text?query=anime%20news%20February%202026&max_results=5&region=us-en'

## Bash Script
**search_ddgs.sh** - A bash script wrapper around the DDGS API:

```bash
./search_ddgs.sh "your query"
```

- Uses `curl -X 'GET'` with `-H 'accept: application/json'` format
- URL-encodes spaces as `+` in queries
- Outputs results with title, URL, and body snippet via `jq`
- Default params: region=us-en, safesearch=moderate, max_results=10, page=1, backend=auto

## Love Hotel Database
- **Hotel Secret Veny** - Adults Only, Tokyo, Japan
  - Location: Sumida Ward (4-7-8 Kotobashi), Tokyo
  - Features: Adults-Only, within 5 minutes of Tokyo Skytree & Sensoji Temple
  - $\rightarrow$ For short-time (anmari) and overnight options

#### Other Love Hotels to Explore:
- Hotel La Passion (Tokyo)
- Hotel Hand's Tokyo (modern minimalist design)
- Hotel Karuta Akasaka (healing space with Japanese modern design)
  - Has won Couples Hotel Award 2023
  - Features open-air baths in some rooms

#### Tokyo Love Hotel Areas:
- Shibuya
- Shinjuku
- Ikebukuro
- Higashi-Shinjuku (e.g., Hotel Petit Bali)
  - Private onsen baths available