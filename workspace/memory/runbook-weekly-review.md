# Runbook: Weekly Review

_Checklist for analytics-brain every Monday. Full analysis cycle._

## Data Collection (Step 1)

- [ ] Pull 7-day Meta data: campaign, ad set, ad level
- [ ] Pull 7-day Google data: campaign, ad group, search terms
- [ ] Pull audience breakdown by country
- [ ] Note any API errors or missing data

## Performance Analysis (Step 2)

- [ ] Rank all ads by CPL (best → worst)
- [ ] Identify top 3 performers (copy pattern)
- [ ] Identify bottom 3 performers (pause candidates)
- [ ] Compare week-over-week trends: CPL, CTR, spend, leads
- [ ] Check frequency on all ad sets (>3.0 = fatigue warning)

## Creative Analysis (Step 3)

- [ ] Which copy frameworks won? (AIDA vs PAS vs BAB vs Social Proof vs Direct)
- [ ] Which image styles performed best? (drone vs lifestyle vs property)
- [ ] Which headlines had highest CTR?
- [ ] Which CTAs converted best?
- [ ] Any creative fatigue signals? (CTR declining, frequency rising)

## Audience Analysis (Step 4)

- [ ] Which countries convert cheapest?
- [ ] Which interest segments perform best?
- [ ] Retargeting vs prospecting performance ratio
- [ ] Any audience saturation? (impressions plateauing, CPL rising)

## Budget Analysis (Step 5)

- [ ] Total spend vs weekly budget
- [ ] ROI by platform (Meta vs Google)
- [ ] Cost trend (improving or worsening?)
- [ ] Recommended budget shifts

## Memory Updates (Step 6) — CRITICAL

After analysis, update these files:

### audiences.md
- New rules confirmed by data → move from Hypotheses to Active Rules
- Disproven hypotheses → move to Archived with reason
- New patterns discovered → add to Hypotheses

### creatives.md
- Winning creatives → add to Winning Creatives table
- Failed creatives → add to Failed Creatives table
- New creative rules → add to appropriate section

### learnings.md
- Update all relevant categories with new findings
- Move confirmed patterns to Active Rules
- Record failed experiments with reasons

### campaign-log.md
- Update CPL 7d column for all active campaigns
- Move completed/paused campaigns to Completed section

## Recommendations (Step 7)

- [ ] Top 3 actions for next week (specific and actionable)
- [ ] Budget reallocation recommendations
- [ ] New A/B tests to run
- [ ] Creatives to pause or rotate

## Report Output

Save to `~/drafts/analytics/weekly/YYYY-WNN.md` using the weekly report format from SKILL.md.

## Learning Cycle Status

After each review, check:
- How many Hypotheses were confirmed/rejected this week?
- Are Active Rules still holding up?
- Any rules that need revision based on new data?
- What's the biggest unknown we should test next?
