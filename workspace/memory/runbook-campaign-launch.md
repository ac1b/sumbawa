# Runbook: Campaign Launch

_Checklist for ad-manager before and after creating any campaign. Read this EVERY time._

## Pre-Launch Checklist

### 1. Read Memory
- [ ] Read `memory/audiences.md` — Active Rules section
- [ ] Read `memory/creatives.md` — Active Rules + Winning Creatives
- [ ] Read `memory/platform-rules.md` — all Active Rules
- [ ] Read `skills/ad-analytics/references/learnings.md` — what worked/failed before

### 2. Strategy Check
- [ ] Campaign objective matches funnel stage (awareness → consideration → conversion)
- [ ] Audience is defined (from audiences.md or new hypothesis)
- [ ] Budget is within approved range (start $5-10/day, confirm with ac1b if > $20/day)
- [ ] Creative is ready (copy + images/video from creative-generator)
- [ ] Landing page is ready (sumbawa.estate or lead form)

### 3. Platform Compliance
- [ ] **Meta**: HOUSING special ad category is set
- [ ] **Meta**: No age/gender/zip targeting (HOUSING restriction)
- [ ] **All**: No "buy land", "own land", guaranteed ROI in copy
- [ ] **Google**: No excessive caps, no exclamation in headlines
- [ ] Campaign created in **PAUSED** status

### 4. Tracking
- [ ] Meta Pixel is installed on landing page (if website CTA)
- [ ] Google conversion tracking is set up (if Google campaign)
- [ ] UTM parameters are in place

## Launch Steps

1. Create campaign via API — **PAUSED**
2. Log action to `~/drafts/ad-cabinet/action-log.md`
3. Create campaign record: `memory/campaigns/{SLUG}.md`
4. Update `memory/campaigns/campaign-log.md` table
5. Notify ac1b: "Campaign {name} created and paused. Ready for review."
6. Wait for ac1b approval before activating
7. After activation: verify delivery starts within 1h

## Post-Launch Monitoring (First 48h)

- [ ] Check impressions at +2h, +6h, +24h, +48h
- [ ] Verify budget spending is on track (not over/under)
- [ ] Check CTR vs benchmarks (>1% Meta, >3% Google Search)
- [ ] Watch for ad rejections or policy warnings
- [ ] If zero delivery after 6h → investigate (audience too small? bid too low? policy rejection?)

## Campaign Record Template

Create `memory/campaigns/{SLUG}.md`:

```markdown
# Campaign: {SLUG}

- **Platform**: Meta / Google
- **Type**: Awareness / Leads / Conversion / Search / PMax
- **Audience**: {audience ID and description}
- **Budget**: ${N}/day
- **Creative**: {link to creative in drafts/}
- **Created**: YYYY-MM-DD
- **Status**: PAUSED → ACTIVE (date) → PAUSED/COMPLETED (date)

## Performance Log

| Date | Spend | Impressions | Clicks | CTR | Leads | CPL | Notes |
|------|-------|-------------|--------|-----|-------|-----|-------|

## Learnings

- [what we learned from this campaign]

## Changes Made

- [YYYY-MM-DD] Created, paused
- [YYYY-MM-DD] Activated by ac1b
```
