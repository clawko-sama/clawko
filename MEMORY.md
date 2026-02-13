## DDGS API - Working Search Methods ✅

**Service Location:** localhost:8000
**Best Practice:** Use curl instead of web_fetch for localhost (direct HTTP access, no MCP mapping)
**Status:** Successfully integrated and tested

**Available Endpoints:**
- GET /search/text (query params) ✅ WORKING
- GET /search/news (query params) ✅ WORKING  
- GET /search/images (query params) ✅ WORKING
- POST /search/text (JSON body) ✅ WORKING
- POST /search/news (JSON body) ✅ WORKING
- GET /search/videos (query params) ✅ WORKING
- GET /search/books (query params) ✅ WORKING

**Working curl commands discovered:**
```bash
curl -X 'GET' 'http://localhost:8000/search/text?query=anime&region=us-en&safesearch=moderate&max_results=10&page=1&backend=auto' -H 'accept: application/json'

curl -s 'http://localhost:8000/search/text?query=love%20hotel%20tokyo&max_results=5&region=us-en'
curl -s 'http://localhost:8000/search/text?query=Hotel%20Secret%20Tokyo&max_results=5&region=us-en'
```

## Love Hotel Research ✅

**Hotels Found & Saved:**

- **Hotel Secret Veny** - Adults Only, Tokyo, Japan
  - Location: Sumida Ward (4-7-8 Kotobashi), Tokyo
  - Features: Adults-Only, within 5 minutes of Tokyo Skytree & Sensoji Temple
  - Type: Short-time (anmari) and overnight options available

- **Hotel La Passion** - Tokyo
- **Hotel Hand's Tokyo** - Modern minimalist design, clean functional spaces
- **Hotel Karuta Akasaka** - Healing space, Japanese modern design
  - Awarded Couples Hotel Award 2023
  - Features open-air baths in some rooms
  - Rooms 2 private onsen baths available in King Suite

- **Hotel Petit Bali Higashi-Shinjuku** - Romantic ambiance
  - 6 room types available
  - Private open-air baths in 3 room types
  - Near Higashi-Shinjuku station

**Tokyo Love Hotel Areas:**
- Shibuya
- Shinjuku
- Ikebukuro 
- Higashi-Shinjuku

**Reference Sites with Full Guides:**
- Tokyo Cheapo - Complete guide to Tokyo love hotels
- Live Japan - Complete guide with booking info
- MATCHA - Top 10 love hotels with features and history
- Tokyo Candies - Coolest love hotels 2025