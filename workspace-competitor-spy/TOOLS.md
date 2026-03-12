# TOOLS.md - Competitor Spy Tools

## Scraper API (primary tool)
- Health: `curl -s http://scraper:8100/health`
- Fetch (fast): `curl -s -X POST http://scraper:8100/fetch -H "Content-Type: application/json" -d "{\"url\":\"...\",\"stealth\":false}"`
- Fetch (stealth): `curl -s -X POST http://scraper:8100/fetch -H "Content-Type: application/json" -d "{\"url\":\"...\",\"stealth\":true,\"timeout\":30000}"`
- CSS selector: add `"selector":".card h2"` to JSON body
- Meta Ad Library: `curl -s -X POST http://scraper:8100/search -H "Content-Type: application/json" -d "{\"search_terms\":\"...\",\"country\":\"ID\",\"limit\":50}"`

## DuckDuckGo (fallback for search)
Google blocks with 429. Use:
```
curl -s -X POST http://scraper:8100/fetch -H "Content-Type: application/json" -d "{\"url\":\"https://duckduckgo.com/?q=QUERY\",\"stealth\":true}"
```

## RETRY LIMIT
- Maximum 3 attempts per URL
- stealth:true hangs → stealth:false
- Website doesn't respond → skip, note it
- After 3 failures → STOP, report

## Results
All reports go to `~/drafts/ad-spy/`:
- `YYYY-MM-DD-scan.md` — competitor scan
- `YYYY-MM-DD-prices.md` — prices
- `YYYY-MM-DD-seo.md` — SEO analysis
