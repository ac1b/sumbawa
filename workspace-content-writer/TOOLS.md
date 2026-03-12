# TOOLS.md - Content Writer Tools

## Scraper API (for topic research)
- Health: `curl -s http://scraper:8100/health`
- Fetch: `curl -s -X POST http://scraper:8100/fetch -H "Content-Type: application/json" -d "{\"url\":\"...\",\"stealth\":false}"`
- Stealth: `curl -s -X POST http://scraper:8100/fetch -H "Content-Type: application/json" -d "{\"url\":\"...\",\"stealth\":true,\"timeout\":30000}"`

## Reference Files (read BEFORE every task)
- `/root/.openclaw/workspace/skills/content-creator/references/style-guide.md`
- `/root/.openclaw/workspace/skills/content-creator/references/content-strategy.md`
- `/root/.openclaw/workspace/skills/content-creator/references/competitors.md`

## RETRY LIMIT
- Maximum 3 attempts per URL/endpoint
- After an error — read the text, understand the cause
- After 3 failures — STOP, report the error

## Results
All materials go to `~/drafts/`:
- `YYYY-MM-DD-topic.md` — finished content
- Format: headline, body, hashtags, CTA

## FORBIDDEN
- Calls to `graph.facebook.com` — that's ad-manager's job
- Creating/modifying ad campaigns — that's ad-manager's job
- Metrics analytics — that's analytics-brain's job
