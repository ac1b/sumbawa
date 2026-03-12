---
name: retargeting-funnel
description: Manages the Sumbawa advertising funnel end-to-end via API — builds custom audiences (video viewers, website visitors, converters), automates funnel stage transitions, and manages messaging sequences across Meta and Google for Sumbawa campaigns. Use when the user mentions "retargeting," "funnel setup," "custom audience," "lookalike audience," "warm audience," or "funnel stage." For general paid advertising strategy and planning, see paid-ads.
metadata:
  openclaw:
    emoji: "\U0001F3AF"
    requires:
      bins:
        - curl
        - jq
---

# Retargeting Funnel — Full-Funnel Ad Automation

You manage the advertising funnel end-to-end. Cold audiences see awareness content, warm audiences get retargeted with details, and hot audiences get conversion-focused ads. The funnel is self-building — each stage feeds the next.

## Reference Files

- `references/funnel-stages.md` — stage definitions, audience rules, messaging
- `../ad-cabinet/references/audiences.md` — audience segments
- `../ad-cabinet/references/campaign-templates.md` — campaign structures
- `../creative-generator/references/frameworks.md` — copy frameworks per stage
- `../ad-analytics/references/learnings.md` — what works at each stage

## The Funnel

```
┌─────────────────────────────────────────────────┐
│  STAGE 1: AWARENESS (Cold)                      │
│  Objective: Video views, reach                  │
│  Content: Drone videos, lifestyle, "did you     │
│           know" posts about Sumbawa             │
│  Audience: Interest-based (broad)               │
│  Budget: 40% of total                           │
│  KPI: CPM, ThruPlay rate, Video view %          │
├─────────────────────────────────────────────────┤
│                    ↓ filter                      │
│  People who watched 75%+ of video               │
│  People who engaged with post                   │
├─────────────────────────────────────────────────┤
│  STAGE 2: CONSIDERATION (Warm)                  │
│  Objective: Traffic, engagement                 │
│  Content: Property carousels, price             │
│           comparisons, testimonials             │
│  Audience: Retarget video viewers +             │
│            website visitors                     │
│  Budget: 35% of total                           │
│  KPI: CTR, CPC, website visits                  │
├─────────────────────────────────────────────────┤
│                    ↓ filter                      │
│  People who visited sumbawa.estate              │
│  People who viewed property pages               │
│  People who spent 30+ sec on site               │
├─────────────────────────────────────────────────┤
│  STAGE 3: CONVERSION (Hot)                      │
│  Objective: Leads                               │
│  Content: Lead forms, "schedule a call",        │
│           investment brochure download,          │
│           WhatsApp direct                       │
│  Audience: Retarget website visitors +          │
│            lookalikes of converters             │
│  Budget: 25% of total                           │
│  KPI: CPL, conversion rate, lead quality        │
└─────────────────────────────────────────────────┘
```

## Custom Audiences to Create

### Meta Custom Audiences

Create these audiences via the Meta API. They auto-populate as people interact with our ads.

```bash
# Video viewers (75%+) — feeds Stage 2
curl -s -X POST "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/customaudiences" \
  -d "name=Funnel - Video Viewers 75%" \
  -d "subtype=ENGAGEMENT" \
  -d "rule={\"inclusions\":{\"operator\":\"or\",\"rules\":[{\"event_sources\":[{\"id\":\"${META_PAGE_ID}\",\"type\":\"page\"}],\"retention_seconds\":2592000,\"filter\":{\"operator\":\"and\",\"filters\":[{\"field\":\"event\",\"operator\":\"eq\",\"value\":\"video_watched\"},{\"field\":\"video_watched.video_p75\",\"operator\":\"eq\",\"value\":\"true\"}]}}]}}" \
  -d "access_token=${META_ADS_ACCESS_TOKEN}"

# Website visitors (all) — feeds Stage 3
curl -s -X POST "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/customaudiences" \
  -d "name=Funnel - Website Visitors 30d" \
  -d "subtype=WEBSITE" \
  -d "rule={\"inclusions\":{\"operator\":\"or\",\"rules\":[{\"event_sources\":[{\"id\":\"${META_PIXEL_ID}\",\"type\":\"pixel\"}],\"retention_seconds\":2592000,\"filter\":{\"operator\":\"and\",\"filters\":[{\"field\":\"url\",\"operator\":\"i_contains\",\"value\":\"sumbawa.estate\"}]}}]}}" \
  -d "access_token=${META_ADS_ACCESS_TOKEN}"

# Property page viewers — high-intent subset
# Similar to above but filter url contains "/property" or "/plots"

# Converters (exclude from prospecting)
# People who triggered Lead event on Meta Pixel

# Lookalike (1%) of converters — feeds Stage 1 + Stage 3
curl -s -X POST "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/customaudiences" \
  -d "name=Funnel - Lookalike 1% Converters" \
  -d "subtype=LOOKALIKE" \
  -d "origin_audience_id={CONVERTERS_AUDIENCE_ID}" \
  -d "lookalike_spec={\"type\":\"similarity\",\"ratio\":0.01,\"country\":\"AU\"}" \
  -d "access_token=${META_ADS_ACCESS_TOKEN}"
```

### Google Remarketing Lists

- All website visitors (Google Ads tag)
- Property page viewers
- Form abandoners (started checkout/form but didn't submit)
- Converters (for Similar Audiences and exclusion)

## Messaging by Stage

### Stage 1: Awareness — "Introduce the dream"

**Tone**: Inspirational, curiosity-driven
**Framework**: AIDA (Attention → Interest)
**Format**: Video (drone), Reels, Stories

Content themes:
- "33km of untouched coast" (aerial drone)
- "15+ world-class surf breaks" (surf footage)
- "The next frontier" (before/after Bali comparison)
- "What $45K buys you in West Sumbawa" (property tour)

**DO**: Inspire, educate, create curiosity
**DON'T**: Sell hard, show prices (too early), use lead forms

### Stage 2: Consideration — "Show the details"

**Tone**: Informative, data-driven
**Framework**: BAB (Before → After → Bridge) or Social Proof
**Format**: Carousel, single image with data, comparison infographic

Content themes:
- Property carousel (each card = different angle/plot)
- Price comparison table (Bali vs Sumbawa)
- Infrastructure update (airport progress)
- "How foreigners invest in Indonesia" (legal guide teaser)
- Testimonials / investor stories (when available)

**DO**: Show specifics — price/sqm, plot sizes, location
**DON'T**: Pressure to buy, use urgency tactics

### Stage 3: Conversion — "Make it easy to act"

**Tone**: Direct, helpful, friction-reducing
**Framework**: PAS (Problem → Agitate → Solution) or Direct
**Format**: Lead form, single image + CTA, "Message us on WhatsApp"

Content themes:
- "Get the free investment brochure"
- "Schedule a virtual site tour"
- "Talk to our team on WhatsApp"
- "Limited plots available — request details"

**DO**: Remove friction, offer value (brochure, consultation), be specific
**DON'T**: Be pushy, create fake urgency

## Funnel Management Workflow

### Setup (one-time)

1. Create all custom audiences (video viewers, website visitors, converters)
2. Create 3 campaign tiers matching funnel stages
3. Set budget allocation: 40% / 35% / 25%
4. Launch Stage 1 campaigns first (need traffic before retargeting works)

### Weekly Maintenance

1. **Check audience sizes**:
   - Video viewers audience > 1,000 → ready to activate Stage 2
   - Website visitors > 500 → ready to activate Stage 3
   - If audiences too small, increase Stage 1 budget
2. **Refresh creatives** every 2-3 weeks per stage (prevent fatigue)
3. **Exclude converters** from all stages (don't keep advertising to people who already inquired)
4. **Move budget** toward whichever stage has best efficiency
5. **Update learnings.md** with funnel-specific insights

### Scaling Rules

| Condition | Action |
|-----------|--------|
| Stage 1 CPM < $10 and ThruPlay > 15% | Increase Stage 1 budget by 20% |
| Video viewer audience > 5,000 | Shift 10% budget from Stage 1 → Stage 2 |
| Website visitors > 2,000 | Shift 10% budget from Stage 2 → Stage 3 |
| Stage 3 CPL < $15 | Scale Stage 3 budget aggressively (up to 50% increase) |
| Any stage frequency > 3.5 | Refresh creatives OR expand audience |
| Stage 3 CPL > $50 for 7 days | Pause Stage 3, focus on building bigger Stage 1/2 audiences |

### Audience Refresh

Audiences decay over time (people lose interest). Maintain freshness:

| Audience | Retention Window | Refresh |
|----------|-----------------|---------|
| Video viewers | 30 days | Rolling (auto) |
| Website visitors | 30 days | Rolling (auto) |
| Property page viewers | 14 days | Rolling (auto) |
| Form abandoners | 7 days | Rolling (auto) |
| Converters (exclude) | 180 days | Rolling (auto) |
| Lookalikes | Rebuild monthly | Manual trigger |

## Cross-Platform Funnel

### Meta → Google → Meta

Full journey:
1. **Meta Stage 1**: Person sees our video on Instagram → watches 75%+
2. **Meta Stage 2**: Person sees carousel ad → clicks → visits sumbawa.estate
3. **Google Stage 3**: Person later searches "sumbawa land investment" → sees our search ad → clicks
4. **Meta Stage 3**: Person gets retargeted with lead form → submits inquiry
5. **Lead captured** → lead-qualifier skill takes over

### Key: Cross-Platform Pixel

Both Meta Pixel AND Google Ads tag must be on sumbawa.estate for cross-platform retargeting to work. Ensure:
- Meta Pixel fires: PageView, ViewContent (property pages), Lead (form submit)
- Google tag fires: page_view, view_item (property pages), generate_lead (form submit)

## Integration with Other Skills

| Skill | How it feeds the funnel |
|-------|----------------------|
| `ad-spy` | Winning competitor patterns → adapt for each funnel stage |
| `creative-generator` | Produces creatives per stage (video for S1, carousel for S2, form for S3) |
| `ad-cabinet` | Executes the actual campaign creation and management |
| `ad-analytics` | Measures performance per stage, identifies bottlenecks |
| `lead-qualifier` | Takes over after Stage 3 conversion — scores and routes leads |
| `content-creator` | Organic content that supports paid funnel (SEO, social posts) |
