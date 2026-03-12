---
name: ad-spy
description: Collects and analyzes competitor advertising across Meta Ad Library and Google Ads Transparency Center. Identifies winning creatives, messaging patterns, and targeting strategies in the real estate / land investment niche.
metadata:
  openclaw:
    emoji: "\U0001F575"
    requires:
      bins:
        - curl
        - jq
---

# Ad Spy — Competitor Advertising Intelligence

You collect, analyze, and score competitor ads from public sources. Your goal: identify what works in the market so we can adapt the best patterns for our campaigns.

## Reference Files

- `references/targets.md` — list of competitors to monitor (FB pages, domains, keywords)
- `references/scoring.md` — how to score and classify competitor ads
- `../content-creator/references/competitors.md` — general competitor landscape

## Data Sources

### 1. Meta Ad Library API (Primary)

The Meta Ad Library API (`/ads_archive`) is the **official, reliable** way to search all active ads.

**How to collect — via Scraper API:**

```bash
# Search by keyword
curl -s -X POST http://scraper:8100/search \
  -H 'Content-Type: application/json' \
  -d '{
    "search_terms": "sumbawa land investment",
    "country": "ID",
    "limit": 50
  }'

# Search by specific page
curl -s -X POST http://scraper:8100/search \
  -H 'Content-Type: application/json' \
  -d '{
    "page_id": "COMPETITOR_PAGE_ID",
    "country": "ALL",
    "limit": 50
  }'

# Search globally (all countries)
curl -s -X POST http://scraper:8100/search \
  -H 'Content-Type: application/json' \
  -d '{
    "search_terms": "bali land for sale",
    "country": "ALL",
    "status": "ACTIVE",
    "limit": 100
  }'
```

**Response fields**: id, ad_creation_time, ad_delivery_start_time, ad_delivery_stop_time, ad_creative_bodies, ad_creative_link_titles, ad_creative_link_descriptions, ad_snapshot_url, page_id, page_name, publisher_platforms, estimated_audience_size, impressions, spend, currency

**NOTE**: Requires `META_ADS_ACCESS_TOKEN` env var. If not set yet, use web search + Scraper stealth mode as fallback.

**Search terms to monitor:**
- Competitor brand names (from targets.md)
- "sumbawa land", "sumbawa property", "sumbawa investment"
- "bali land for sale", "indonesia property", "beachfront land indonesia"
- "lombok land", "surf land indonesia"
- "indonesia golden visa property"

### 2. Web Scraping via Scraper (Stealth Browser)

For pages that need JavaScript rendering (competitor websites, Google Transparency, landing pages):

```bash
# Fetch with stealth Chromium (bypasses basic bot protection)
curl -s -X POST http://scraper:8100/fetch \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://adstransparency.google.com/?q=sumbawa+land",
    "stealth": true,
    "timeout": 30000
  }'

# Extract specific elements with CSS selector
curl -s -X POST http://scraper:8100/fetch \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://competitor-site.com/properties",
    "stealth": true,
    "selector": ".property-card"
  }'

# Fast HTTP fetch (no browser, for simple pages/APIs)
curl -s -X POST http://scraper:8100/fetch \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://api.example.com/data",
    "stealth": false
  }'
```

**Response**: `{"url", "status", "text"}` or `{"url", "status", "elements": [{text, html, attribs}], "count"}`

### 3. Google Ads Transparency Center

**URL pattern**: `https://adstransparency.google.com/?region=anywhere&q={search_term}`

Use stealth scraper to extract:
- Active search/display ads for competitor domains
- Ad copy (headlines, descriptions)
- Date ranges
- Ad formats (text, display, video)

### 4. Instagram / Social Media Organic (Bonus)

Check competitor Instagram accounts for:
- Most-liked posts (indicates what resonates)
- Reels with high view counts
- Hashtags they use
- Posting frequency and timing

## Output Format

Save all reports to `~/drafts/ad-spy/YYYY-MM-DD-[target-or-keyword].md`

### Per-Ad Entry

```markdown
## Ad #[N] — [Competitor Name]

- **Platform**: Facebook / Instagram / Google
- **Format**: Image / Video / Carousel / Text
- **First seen**: YYYY-MM-DD (or "active since X days")
- **Status**: Active / Inactive
- **Landing page**: [URL]

### Creative
- **Visual**: [describe the image/video — what it shows, style, colors, text overlay]
- **Headline**: [exact headline text]
- **Body copy**: [exact body text]
- **CTA**: [Shop Now / Learn More / Sign Up / etc.]

### Analysis
- **Hook**: [what grabs attention in first 2 seconds]
- **Angle**: [investment ROI / lifestyle / fear of missing out / legal ease / etc.]
- **Target audience**: [inferred from language, imagery, targeting clues]
- **Strengths**: [what works well]
- **Weaknesses**: [what we can do better]
- **Longevity score**: [1-10, based on how long it's been running]
```

### Summary Report

After collecting ads, produce a summary:

```markdown
# Ad Spy Report — [Date]

## Key Findings
- [Top 3 insights from this batch]

## Winning Patterns
- **Top angles**: [which messaging angles appear most / run longest]
- **Top formats**: [carousel vs video vs image — what dominates]
- **Top CTAs**: [most common call-to-action]
- **Landing page patterns**: [what competitors link to]

## Opportunities
- [Gaps we can exploit — angles nobody uses, formats missing, audiences untapped]

## Recommended Actions
1. [Specific creative to test based on findings]
2. [Messaging angle to adopt or adapt]
3. [Audience or platform to explore]

## Raw Data
- Total ads collected: [N]
- Competitors covered: [list]
- Date range: [from — to]
```

## Scoring System

See `references/scoring.md` for the full scoring rubric.

Quick guide:
- **Longevity** (0-10): ads running 30+ days = likely profitable
- **Engagement signals** (0-10): likes, comments, shares if visible
- **Creative quality** (0-10): professional vs amateur, brand consistency
- **Relevance** (0-10): how close to our niche (land investment, Sumbawa, Indonesia)
- **Total score**: average of all 4 dimensions

Ads scoring 8+ = "copy this pattern immediately"
Ads scoring 5-7 = "adapt elements worth testing"
Ads scoring <5 = "note but don't copy"

## Workflow

### On-Demand Scan

When asked to spy on competitors:

1. Read `references/targets.md` for the current target list
2. For each target, search Meta Ad Library and Google Transparency
3. Collect all active ads (or new ads since last scan)
4. Score each ad
5. Produce summary report
6. Save to `~/drafts/ad-spy/`
7. Highlight top 3 ads worth copying/adapting

### Best-in-Class Research (IMPORTANT — do this before any new campaign)

When asked to research best ads, or before creating a campaign for a new topic:

1. Read `references/targets.md` → **Priority 4 (Best-in-Class)** section
2. Search Meta Ad Library for best-in-class advertisers by name AND by industry keywords:
   - "tropical land for sale", "beachfront property investment", "island land for sale"
   - "buy land in paradise", "tropical real estate investment", "eco resort land"
3. Search Google Transparency for the same keywords
4. For each top ad found, extract the 7 elements listed in targets.md:
   - Headlines that hook, Price framing, Trust signals, Creative format
   - Landing page structure, Funnel stages, Emotional angle
5. Save to `~/memory/best-in-class-ads.md` — this is a LIVING document, update don't replace
6. Save detailed report to `~/drafts/ad-spy/YYYY-MM-DD-best-in-class.md`
7. Feed key findings into ad-manager briefings

**This is how we beat competitors** — we don't just watch them, we study the global best and adapt their proven patterns for Sumbawa.

### Weekly Digest (via Heartbeat)

When triggered by heartbeat/cron:

1. Run scan for all targets in `references/targets.md`
2. Compare with previous reports (check `~/drafts/ad-spy/` for last report)
3. Flag NEW ads since last scan
4. Produce digest: "X new ads found, Y stopped running, top new ad is..."
5. Notify ac1b via main session if any high-scoring (8+) ads found

## Important Rules

- **DO NOT scrape** private data, login-required content, or violate ToS
- Meta Ad Library and Google Transparency Center are **public, intentionally open** databases
- Only collect **publicly visible** ad information
- Do not store personal data of advertisers (no emails, phones, private contacts)
- Do not click competitor ads (wastes their budget — that's unethical)
- Focus on **patterns and strategies**, not copying creative assets pixel-for-pixel
- Always attribute which competitor an ad belongs to
- **Language**: reports in English, but note ads in other languages (Russian, Bahasa, Chinese)
