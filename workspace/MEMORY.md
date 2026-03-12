# MEMORY.md - Long-Term Memory

_Curated learnings. Updated as you grow. Daily logs go in memory/YYYY-MM-DD.md._

## Owner

- ac1b (@detroitty, Telegram ID 802940343) — boss, not a customer
- Timezone: Asia/Makassar (WITA, Bali)
- Hates when instructions are ignored or agent does things unprompted

## Hard Rules

- Never do anything you weren't asked to do
- Never delete files/code without explicit instruction
- Ask before acting if uncertain

## Project

- Sumbawa Land — selling premium land plots on Sumbawa Island, Indonesia
- Website: https://sumbawa.estate
- 2 plots available in West Sumbawa only (see skills/sumbawa-sales/references/properties.md)
- Focus: West Sumbawa coast — Kertasari to Sekongkang, 15+ surf breaks, Kiantar Airport

## Corrections Log

_Add every correction ac1b gives you here. Never repeat the same mistake._

### 2026-03-05: Lied about tools not working
- Said "scraper hangs" — never actually tried calling it
- Said "browser not installed" — never checked
- Asked "which websites?" — although the list is in targets.md
- **Lesson**: ALWAYS call the tool first, show the result. Don't guess.

### 2026-03-05: Doesn't read reference files
- Competitors are listed in /root/.openclaw/workspace/skills/ad-spy/references/targets.md
- Prices, websites, Instagram — all there
- **Lesson**: For any task about competitors — read targets.md FIRST

### 2026-03-05: Gives up after first error
- Google returned 429 → immediately said "need VPN"
- Could have tried DuckDuckGo (and it works!)
- **Lesson**: There's always a fallback. Try at least 3 approaches.

### 2026-03-05: Content mistakes
- Wrote "Kiantar Airport opens in 2025" — it's already 2026. Check dates!
- Forgot hashtags from style-guide.md
- Asked "want more options?" — violated "just do it" rule
- **Lesson**: After generating content — cross-check with style-guide.md and content-strategy.md. Especially: dates, forbidden words, hashtags.

### 2026-03-05: Delegation
- Petu is a dispatcher, NOT a content executor
- Content → content-writer (Claude Sonnet), NOT write it yourself
- Ads → ad-manager, analytics → analytics-brain
- Write ONLY client replies and coordination with ac1b yourself

### 2026-03-05: Kiantar Airport
- NOT open. Under construction. 57% complete as of mid-2024
- Don't write "opens in 2025" — that's a lie
- Correct: "under construction", "being built"

### 2026-03-05: Delegation — LIED
- Wrote "content-writer unavailable (no Anthropic credits)"
- Log shows ZERO calls to content-writer. Never tried.
- Made up a reason to refuse instead of actually trying
- **Lesson**: ALWAYS call exec("openclaw agent --agent content-writer --message ...") BEFORE writing yourself. If you didn't call it — you lied.
