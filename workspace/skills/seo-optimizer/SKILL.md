---
name: seo-optimizer
description: Analyzes Google SERP rankings for Sumbawa target keywords (e.g. "sumbawa land for sale," "west sumbawa property"), compares sumbawa.estate content against top-ranking competitors, and suggests specific content improvements. Use when optimizing Sumbawa website content for specific keywords. Also use when the user mentions "check our rankings," "keyword position," "SERP analysis," or "optimize for [keyword]." For a comprehensive technical SEO audit, see seo-audit. For AI search optimization (ChatGPT, Perplexity), see ai-seo.
metadata:
  openclaw:
    emoji: "\U0001F50D"
    requires:
      bins:
        - curl
---

# SEO Optimizer

You analyze search engine rankings for target keywords and optimize our content to rank higher.

## Process

When asked to optimize for a keyword:

1. **Search** — use web search to find the top 10 results for the target keyword
2. **Analyze competitors** — fetch and analyze the top 3-5 ranking pages:
   - Word count
   - Heading structure (H1, H2, H3)
   - Key topics covered
   - Internal/external link count
   - Content format (listicle, guide, comparison, etc.)
3. **Compare** — identify gaps between our content and top rankers
4. **Recommend** — provide specific, actionable improvements

## References

- `../content-creator/references/competitors.md` — who ranks for our keywords
- `../content-creator/references/content-strategy.md` — keyword and platform strategy

## Output Location

Save reports to `~/drafts/seo/YYYY-MM-DD-[keyword-slug].md`

## Target Keywords

### Primary (high priority)
- "sumbawa land for sale"
- "invest in sumbawa land"
- "sumbawa island property"
- "beachfront land indonesia"

### Secondary
- "indonesia land investment 2026"
- "sumbawa real estate"
- "cheap beachfront land asia"
- "west sumbawa land for sale"
- "sumbawa property investment"

### Long-tail (high intent)
- "can foreigners buy land in indonesia"
- "how to invest in land in indonesia as foreigner"
- "sumbawa vs bali land prices"
- "best islands to invest in land southeast asia"
- "PT PMA indonesia property"
- "indonesia golden visa property"
- "cheapest beachfront land in indonesia"
- "sumbawa new airport land prices"

### Russian-language keywords
- "земля на сумбаве купить"
- "инвестиции в землю индонезия"
- "участок на берегу индонезия"

## Output Format

```markdown
## SEO Analysis: [keyword]

### Current State
- Our ranking: [position or "not found"]
- Our page: [URL]
- Word count: [number]

### Top Competitors
| # | URL | Words | Topics | Backlinks |
|---|-----|-------|--------|-----------|
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |

### Content Gaps
- [Topic covered by competitors but not us]
- [Question answered by competitors but not us]
- [Data/stats included by competitors but not us]

### Recommendations
1. [Specific change with expected impact]
2. [Specific change with expected impact]
3. [Specific change with expected impact]

### Suggested New Sections
- [H2: Section Title] — [brief description of content to add]
```

## Rules

- Always use web search for current SERP data — never rely on assumptions
- Focus on content quality improvements, not technical SEO hacks
- Recommend content additions, not keyword stuffing
- Consider search intent: informational vs transactional
- Prioritize improvements with highest impact-to-effort ratio
- Check if our website (sumbawa.estate) appears in results and at what position
