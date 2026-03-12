---
name: ad-analytics
description: Pulls performance data from Meta and Google ad accounts, analyzes trends, detects problems, recommends optimizations, and learns from historical results. Produces daily/weekly reports and self-improving strategy recommendations.
metadata:
  openclaw:
    emoji: "\U0001F4CA"
    requires:
      bins:
        - curl
        - jq
---

# Ad Analytics — Performance Intelligence & Self-Learning

You are the brain of the advertising system. You pull data, find patterns, detect problems early, and continuously improve our ad strategy based on what actually works.

## Reference Files

- `references/kpis.md` — target KPIs, benchmarks, and alert thresholds
- `references/learnings.md` — accumulated learnings (self-updating knowledge base)
- `../ad-cabinet/references/platforms.md` — API endpoints for pulling data
- `../ad-cabinet/references/audiences.md` — audience definitions
- `../ad-cabinet/references/campaign-templates.md` — campaign structures

## Output Location

- Daily reports: `~/drafts/analytics/daily/YYYY-MM-DD.md`
- Weekly reports: `~/drafts/analytics/weekly/YYYY-WNN.md`
- Learnings: `references/learnings.md` (update in-place)

## Data Collection

### Meta Ads — Pull Insights

```bash
# Campaign-level performance (last 7 days)
curl -s "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/insights?\
fields=campaign_name,impressions,reach,clicks,ctr,cpc,spend,\
actions,cost_per_action_type,frequency\
&date_preset=last_7d\
&level=campaign\
&access_token=${META_ADS_ACCESS_TOKEN}" | jq '.'

# Ad-level performance (to identify winning creatives)
curl -s "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/insights?\
fields=ad_name,impressions,clicks,ctr,cpc,spend,actions,cost_per_action_type\
&date_preset=last_7d\
&level=ad\
&access_token=${META_ADS_ACCESS_TOKEN}" | jq '.'

# Audience breakdown
curl -s "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/insights?\
fields=impressions,clicks,spend,actions\
&date_preset=last_7d\
&breakdowns=country\
&access_token=${META_ADS_ACCESS_TOKEN}" | jq '.'
```

### Google Ads — Pull via GAQL

```bash
# Refresh OAuth token first (see platforms.md)

# Campaign performance
# IMPORTANT: login-customer-id header is REQUIRED (MCC manager ID)
curl -s -X POST "https://googleads.googleapis.com/v20/customers/${GOOGLE_ADS_CUSTOMER_ID}/googleAds:searchStream" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT campaign.name, metrics.impressions, metrics.clicks, metrics.ctr, metrics.cost_micros, metrics.conversions, metrics.cost_per_conversion FROM campaign WHERE segments.date DURING LAST_7_DAYS AND campaign.status = ENABLED"}'

# Search terms (what people actually typed)
# ... query: "SELECT search_term_view.search_term, metrics.impressions, metrics.clicks, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_7_DAYS ORDER BY metrics.impressions DESC"
```

## Analysis Framework

### Daily Check (5-minute scan)

Run every day. Quick health check:

1. **Pull last 24h data** from both platforms
2. **Compare to KPI targets** (see kpis.md)
3. **Flag anomalies**:
   - Spend > 120% of daily budget → ALERT
   - CTR dropped > 30% vs 7-day average → WARNING
   - CPL spiked > 2x vs 7-day average → ALERT
   - Zero impressions on active campaign → CRITICAL
   - Frequency > 3.0 → WARNING (audience fatigue)
4. **Quick summary**: 3-5 bullet points + any actions needed

### Weekly Deep Dive

Run every Monday. Full analysis:

1. **Pull 7-day data** at campaign, ad set, and ad level
2. **Performance ranking**: sort all ads by CPL (best → worst)
3. **Creative analysis**:
   - Which copy variants won? (compare A/B test results)
   - Which image styles performed best?
   - Which headlines had highest CTR?
4. **Audience analysis**:
   - Which countries convert cheapest?
   - Which interest segments perform best?
   - Is retargeting outperforming prospecting?
5. **Budget analysis**:
   - Total spend vs budget
   - ROI by platform (Meta vs Google)
   - Cost trend (improving or worsening week over week?)
6. **Competitor context**: reference latest ad-spy report
7. **Recommendations**: top 3 actions for next week
8. **Update learnings.md** with new findings

### Monthly Strategy Review

Run first Monday of month:

1. **Full month performance** vs targets
2. **Trend analysis**: CPL, CTR, conversion rate over time
3. **Audience evolution**: are certain segments saturating?
4. **Creative lifecycle**: which creatives are fatiguing?
5. **Budget reallocation**: shift spend to what works
6. **Strategy adjustment**: update KPIs, audiences, or approach based on data
7. **Major update to learnings.md**

## Report Format

### Daily Report

```markdown
# Daily Ad Report — [Date]

## Summary
- **Total spend**: $X (Meta: $X, Google: $X)
- **Leads**: N (CPL: $X)
- **Clicks**: N (CTR: X%)
- **Status**: 🟢 On track / 🟡 Watch / 🔴 Action needed

## Alerts
- [any anomalies or issues]

## Top Performer
- [best ad today with stats]

## Action Items
- [ ] [what to do]
```

### Weekly Report

```markdown
# Weekly Ad Report — Week [N], [Date Range]

## Executive Summary
[3 sentences: what happened, what worked, what to change]

## Performance Table

| Campaign | Spend | Impressions | Clicks | CTR | Leads | CPL | ROAS |
|----------|-------|-------------|--------|-----|-------|-----|------|
| ... | ... | ... | ... | ... | ... | ... | ... |

## Winners & Losers

### Top 3 Ads (by CPL)
1. [ad name] — CPL $X, CTR X%, [why it works]
2. ...
3. ...

### Bottom 3 Ads (consider pausing)
1. [ad name] — CPL $X, CTR X%, [what's wrong]
2. ...
3. ...

## Audience Insights
- Best country: [country] (CPL $X)
- Best segment: [segment] (CPL $X)
- Fatigue warning: [segment] frequency > 3.0

## Creative Insights
- Winning angle: [which messaging worked]
- Winning format: [carousel / video / image]
- Winning hook: [which first line got clicks]

## Recommendations
1. [action + expected impact]
2. [action + expected impact]
3. [action + expected impact]

## Budget Recommendation
- Current: $X/day
- Recommended: $X/day
- Reason: [why]
```

## Self-Learning System

### How It Works

The `references/learnings.md` file is a **cumulative knowledge base** that grows over time. After every weekly analysis:

1. **Record what worked** — specific ads, angles, audiences, formats
2. **Record what failed** — and WHY (not just "bad CTR" but "audience too broad" or "copy too generic")
3. **Update rules** — e.g., "Australian audience converts 2x cheaper than US → prioritize AU budget"
4. **Track patterns** — "carousel outperforms single image by 40% on average"
5. **Revise predictions** — update expected CPL, CTR baselines as data accumulates

### Learning Categories

```markdown
## Audiences
- [what we learned about which audiences work]

## Creative
- [what copy/image patterns win]

## Timing
- [best days/times for engagement]

## Platform
- [Meta vs Google findings]

## Budget
- [optimal spend levels, scaling thresholds]

## Seasonal
- [any time-of-year patterns]
```

### Feeding Learnings Back

When creating new campaigns or creatives, ALWAYS:
1. Read `references/learnings.md` first
2. Apply known winning patterns
3. Avoid known failing patterns
4. Test ONE new variable at a time against proven winners

This creates a feedback loop:
```
Create → Measure → Learn → Apply → Create better → Measure → Learn more
```

## Alert Escalation

| Severity | Condition | Action |
|----------|-----------|--------|
| 🔴 CRITICAL | Zero delivery, budget overspend, account issues | Notify ac1b immediately |
| 🟡 WARNING | CPL spike, CTR drop, frequency high | Include in daily report, suggest fix |
| 🟢 INFO | Normal fluctuation, minor trends | Include in weekly report |
| ⭐ OPPORTUNITY | CPL unusually low, new winning creative | Suggest scaling, notify ac1b |
