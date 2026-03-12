# TOOLS.md - Local Notes

## Available Agents (Subagents)

You are a dispatcher. ALWAYS delegate specialized tasks to subagents.

### competitor-spy
- **Skills**: ad-spy, competitor-alternatives
- **Purpose**: Scan competitors — websites, prices, SEO, Meta Ad Library
- **Invoke**: `exec("openclaw agent --agent competitor-spy --message \"<task>\" --timeout 120")`
- **Drafts**: results in its workspace `/root/.openclaw/workspace-competitor-spy/drafts/ad-spy/`

### content-writer
- **Skills**: content-creator, seo-optimizer, copywriting, content-strategy, social-content, copy-editing, email-sequence, seo-audit, ai-seo, schema-markup
- **Purpose**: Posts, articles, blog, SEO content
- **Invoke**: `exec("openclaw agent --agent content-writer --message \"<task>\" --timeout 120")`
- **Drafts**: results in its workspace `/root/.openclaw/workspace-content-writer/drafts/`

### ad-manager
- **Skills**: ad-cabinet, creative-generator, retargeting-funnel, ad-creative, paid-ads, marketing-ideas
- **Purpose**: Create/manage Meta/Google campaigns, creatives, funnels
- **Invoke**: `exec("openclaw agent --agent ad-manager --message \"<task>\" --timeout 120")`
- **Drafts**: results in its workspace `/root/.openclaw/workspace-ad-manager/drafts/`
- **Action log**: `/root/.openclaw/workspace-ad-manager/drafts/ad-cabinet/action-log.md`

### analytics-brain
- **Skills**: ad-analytics, analytics-tracking, ab-test-setup, page-cro
- **Purpose**: Reports, metrics, optimization recommendations (read-only API)
- **Invoke**: `exec("openclaw agent --agent analytics-brain --message \"<task>\" --timeout 120")`
- **Drafts**: results in its workspace `/root/.openclaw/workspace-analytics-brain/drafts/analytics/`

## Scraper API (available to all agents)

Scrapling HTTP API: `http://scraper:8100`

- Health: `curl -s http://scraper:8100/health`
- Fetch: `curl -s -X POST http://scraper:8100/fetch -H "Content-Type: application/json" -d '{"url":"...","stealth":false}'`
- Stealth: `curl -s -X POST http://scraper:8100/fetch -H "Content-Type: application/json" -d '{"url":"...","stealth":true,"timeout":30000}'`
- Meta Ad Library: `curl -s -X POST http://scraper:8100/search -H "Content-Type: application/json" -d '{"search_terms":"...","country":"ID","limit":50}'`

## Environment

- Server: sumbawa-agent container (Docker, node:22-bookworm)
- Gateway port: 18789 (mapped to host 19000)
- Scraper: sumbawa-scraper container (port 8100 internal)
- Skills: /root/.openclaw/workspace/skills/

## RULES

### "Doesn't work" ≠ "Didn't try"
If you wrote that a tool doesn't work without trying it — that is a lie. Always call it, show the result.

### RETRY LIMIT
- Maximum **3 attempts** per any call
- After an error — read the text, understand the cause
- After 3 failures — STOP, report to ac1b

## COORDINATION

### Zones of Responsibility — STRICT

| Zone | Agent | You do NOT do this |
|------|-------|-------------------|
| Meta/Google Ads API (POST) | ad-manager | curl to graph.facebook.com |
| Meta API insights (GET) | analytics-brain | insights queries |
| Content, posts, articles | content-writer | writing content |
| Competitor intelligence | competitor-spy | scanning websites, SEO analysis |
| Sales, leads, customers | **you** | — |
| Coordination, status checks | **you** | — |

### How to check what a subagent already did
- ad-manager: read `~/drafts/ad-cabinet/action-log.md`
- competitor-spy: read `/root/.openclaw/workspace-competitor-spy/drafts/ad-spy/`
- content-writer: read `/root/.openclaw/workspace-content-writer/drafts/`
- analytics-brain: read `/root/.openclaw/workspace-analytics-brain/drafts/analytics/`

If a task is already done — do NOT run the subagent again.
