# Platform Rules & Lessons

_Rules learned from experience with ad platforms. Updated when we discover new gotchas._

## Active Rules
_(confirmed by experience or documentation)_

### Meta Ads
- **(2026-03-04, confidence: high, evidence: Meta policy)** HOUSING Special Ad Category is MANDATORY for all real estate ads
- **(2026-03-04, confidence: high, evidence: Meta policy)** HOUSING blocks: age targeting, gender targeting, zip code targeting, min 15-mile radius
- **(2026-03-04, confidence: high, evidence: Meta policy)** Never delete campaigns — pause instead, deleted = gone forever
- **(2026-03-04, confidence: high, evidence: platforms.md)** Long-lived access token expires in 60 days — refresh before expiry
- **(2026-03-04, confidence: high, evidence: platforms.md)** Rate limit: ~200 calls/hour per ad account, insights max 600/5min
- **(2026-03-04, confidence: high, evidence: ad-cabinet/SKILL.md)** Budget increase max 20% at once — Meta penalizes big jumps
- **(2026-03-04, confidence: high, evidence: ad-cabinet/SKILL.md)** ALL campaigns created PAUSED — never launch without ac1b approval
- **(2026-03-04, confidence: high, evidence: ad-cabinet/SKILL.md)** Kill CPL > $50 after 72 hours
- **(2026-03-04, confidence: high, evidence: ad-cabinet/SKILL.md)** Scale CPL < $15 by 20% (max once per 3 days)
- **(2026-03-04, confidence: medium, evidence: best practices)** Frequency > 3.0 = audience fatigue, rotate creative

### Google Ads
- **(2026-03-04, confidence: high, evidence: Google policy)** No excessive capitalization in ad copy
- **(2026-03-04, confidence: high, evidence: Google policy)** No exclamation marks in headlines
- **(2026-03-04, confidence: high, evidence: Google policy)** No misleading claims
- **(2026-03-04, confidence: high, evidence: platforms.md)** Developer token basic access: 15K requests/day, 1K GAQL queries/day
- **(2026-03-04, confidence: high, evidence: platforms.md)** OAuth token must be refreshed before each request

### Legal (Indonesia)
- **(2026-03-04, confidence: high, evidence: brand-rules.md)** NEVER say "buy land" or "own land" — use "invest in", "secure", "leasehold"
- **(2026-03-04, confidence: high, evidence: brand-rules.md)** NEVER guarantee ROI — use "potential", "projections"
- **(2026-03-04, confidence: high, evidence: competitors.md)** Julian Petroulas banned from Indonesia for "How I Make MILLIONS in Bali" — terminology matters legally

## Hypotheses
_(testing, not confirmed)_

- **(2026-03-04)** Meta Advantage+ placements may outperform manual placement selection
- **(2026-03-04)** Google Performance Max may deliver better ROAS than Search for our niche (need to test)

## Archived
_(disproven or outdated)_

- [none yet]
