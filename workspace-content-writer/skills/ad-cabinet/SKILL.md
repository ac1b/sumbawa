---
name: ad-cabinet
description: Executes Meta and Google Ads campaign operations via API for Sumbawa — creates, edits, pauses, and scales live campaigns using curl commands. Use when you need to actually create or modify a campaign in the ad account. Also use when the user mentions "create campaign," "pause campaign," "change budget," "upload creative," "launch ads," or "ad account management." For ad strategy, planning, and campaign structure advice, see paid-ads.
metadata:
  openclaw:
    emoji: "\U0001F4CB"
    requires:
      bins:
        - curl
        - jq
---

# Ad Cabinet — Campaign Management

You manage paid advertising campaigns across Meta (Facebook/Instagram) and Google Ads. You create campaigns, manage budgets, rotate creatives, and control targeting — all through API calls.

## Reference Files

- `references/platforms.md` — API endpoints, auth setup, SDK usage
- `references/campaign-templates.md` — pre-built campaign structures for real estate
- `references/audiences.md` — target audience definitions and segments
- `../ad-spy/references/targets.md` — competitor data for targeting inspiration

## Shared Memory (read before creating campaigns, write after)

- `~/memory/runbook-campaign-launch.md` — **READ THIS BEFORE EVERY CAMPAIGN CREATION**
- `~/memory/audiences.md` — audience knowledge, Active Rules
- `~/memory/platform-rules.md` — platform-specific rules and gotchas
- `~/memory/campaigns/campaign-log.md` — update after creating campaign
- `~/memory/campaigns/{SLUG}.md` — create per-campaign record after launch

## Safety Rules — CRITICAL

1. **ALL campaigns are created in PAUSED status.** Never launch live without ac1b's explicit approval.
2. **Budget changes > $10/day require confirmation.** Ask before increasing spend.
3. **Never delete campaigns.** Pause them instead. Deleted = gone forever.
4. **Log every action.** Write what you did to `~/drafts/ad-cabinet/action-log.md`.
5. **Special Ad Category: HOUSING** is MANDATORY for all Meta real estate ads. This limits targeting (no age, gender, zip code).
6. **Never say "buy land"** in ad copy. Use "invest in", "secure", "leasehold opportunity".

## Platforms

### Meta Ads (Facebook + Instagram)

**Auth**: Meta Marketing API via long-lived access token.
- Token stored in env: `META_ADS_ACCESS_TOKEN`
- Ad Account ID in env: `META_AD_ACCOUNT_ID`
- Page ID in env: `META_PAGE_ID`

**API Base**: `https://graph.facebook.com/v21.0`

**Core operations via curl:**

```bash
# List campaigns
curl -s "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/campaigns?fields=name,status,objective,daily_budget&access_token=${META_ADS_ACCESS_TOKEN}"

# Create campaign (PAUSED)
curl -s -X POST "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/campaigns" \
  -d "name=Sumbawa Land - Investors AU" \
  -d "objective=OUTCOME_LEADS" \
  -d "status=PAUSED" \
  -d "special_ad_categories=[\"HOUSING\"]" \
  -d "access_token=${META_ADS_ACCESS_TOKEN}"

# Get campaign performance
curl -s "https://graph.facebook.com/v21.0/{campaign_id}/insights?fields=impressions,clicks,ctr,spend,actions,cost_per_action_type&date_preset=last_7d&access_token=${META_ADS_ACCESS_TOKEN}"

# Pause campaign
curl -s -X POST "https://graph.facebook.com/v21.0/{campaign_id}" \
  -d "status=PAUSED" \
  -d "access_token=${META_ADS_ACCESS_TOKEN}"
```

### Google Ads

**Auth**: OAuth2 via refresh token.
- Credentials in env: `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID`, `GOOGLE_ADS_LOGIN_CUSTOMER_ID`

**API Base**: `https://googleads.googleapis.com/v20`

**IMPORTANT**: Every Google Ads API request MUST include the `login-customer-id` header set to `${GOOGLE_ADS_LOGIN_CUSTOMER_ID}` (the MCC manager ID). Without it, requests will fail with USER_PERMISSION_DENIED.

**IMPORTANT**: When creating campaigns, you MUST include `"containsEuPoliticalAdvertising": 3` (integer 3 = DOES_NOT_CONTAIN). Without it, the API returns REQUIRED field error.

Google Ads API requires OAuth token refresh before each request:

```bash
# Get access token
ACCESS_TOKEN=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "client_id=${GOOGLE_ADS_CLIENT_ID}" \
  -d "client_secret=${GOOGLE_ADS_CLIENT_SECRET}" \
  -d "refresh_token=${GOOGLE_ADS_REFRESH_TOKEN}" \
  -d "grant_type=refresh_token" | jq -r '.access_token')

# Query campaigns (GAQL)
curl -s -X POST "https://googleads.googleapis.com/v20/customers/${GOOGLE_ADS_CUSTOMER_ID}/googleAds:searchStream" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT campaign.name, campaign.status, metrics.impressions, metrics.clicks, metrics.cost_micros FROM campaign WHERE segments.date DURING LAST_7_DAYS"}'

# --- MUTATE OPERATIONS (create/update/delete) ---
# All mutate requests use: POST /v20/customers/{CID}/{resource}:mutate
# All require: Authorization, developer-token, login-customer-id, Content-Type headers (same as above)

# 1. Create budget (amountMicros = amount × 1,000,000; IDR 300,000/day = 300000000000)
curl -s -X POST "https://googleads.googleapis.com/v20/customers/${GOOGLE_ADS_CUSTOMER_ID}/campaignBudgets:mutate" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"operations": [{"create": {"name": "My Budget", "amountMicros": "300000000000", "deliveryMethod": "STANDARD"}}]}'

# 2. Create Search campaign (PAUSED)
# IMPORTANT: use "manualCpc": {} for bid strategy, "containsEuPoliticalAdvertising": 3
curl -s -X POST "https://googleads.googleapis.com/v20/customers/${GOOGLE_ADS_CUSTOMER_ID}/campaigns:mutate" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"operations": [{"create": {"name": "My Campaign", "advertisingChannelType": "SEARCH", "status": "PAUSED", "campaignBudget": "customers/CID/campaignBudgets/BUDGET_ID", "manualCpc": {"enhancedCpcEnabled": false}, "networkSettings": {"targetGoogleSearch": true, "targetSearchNetwork": false, "targetContentNetwork": false}, "containsEuPoliticalAdvertising": 3}}]}'

# 3. Create Ad Group
curl -s -X POST "https://googleads.googleapis.com/v20/customers/${GOOGLE_ADS_CUSTOMER_ID}/adGroups:mutate" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"operations": [{"create": {"name": "My Ad Group", "campaign": "customers/CID/campaigns/CAMPAIGN_ID", "status": "ENABLED", "type": "SEARCH_STANDARD", "cpcBidMicros": "15000000"}}]}'

# 4. Create Keywords (phrase match)
curl -s -X POST "https://googleads.googleapis.com/v20/customers/${GOOGLE_ADS_CUSTOMER_ID}/adGroupCriteria:mutate" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"operations": [{"create": {"adGroup": "customers/CID/adGroups/AG_ID", "status": "ENABLED", "keyword": {"text": "my keyword", "matchType": "PHRASE"}}}]}'

# 5. Create Responsive Search Ad
curl -s -X POST "https://googleads.googleapis.com/v20/customers/${GOOGLE_ADS_CUSTOMER_ID}/adGroupAds:mutate" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"operations": [{"create": {"adGroup": "customers/CID/adGroups/AG_ID", "status": "ENABLED", "ad": {"responsiveSearchAd": {"headlines": [{"text": "Headline 1"}, {"text": "Headline 2"}, {"text": "Headline 3"}], "descriptions": [{"text": "Description line 1"}, {"text": "Description line 2"}]}, "finalUrls": ["https://example.com"]}}}]}'

# 6. Remove any resource
curl -s -X POST "https://googleads.googleapis.com/v20/customers/${GOOGLE_ADS_CUSTOMER_ID}/campaigns:mutate" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"operations": [{"remove": "customers/CID/campaigns/CAMPAIGN_ID"}]}'

# 7. Update campaign status
curl -s -X POST "https://googleads.googleapis.com/v20/customers/${GOOGLE_ADS_CUSTOMER_ID}/campaigns:mutate" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"operations": [{"update": {"resourceName": "customers/CID/campaigns/CAMPAIGN_ID", "status": "ENABLED"}, "updateMask": "status"}]}'
```

## Campaign Structure

### Meta Ads Structure

```
Campaign (objective + budget + special_ad_category)
  └── Ad Set (audience + placement + schedule + bid)
       └── Ad (creative: image/video + copy + CTA + landing page)
```

### Google Ads Structure

```
Campaign (type + budget + bid strategy + geo targeting)
  └── Ad Group (keywords + audience)
       └── Ad (responsive search ad: headlines + descriptions + URL)
```

## Campaign Templates for Sumbawa

### Template 1: Meta — Awareness (Video Views)

**Objective**: OUTCOME_AWARENESS
**Format**: Video (drone footage of coast / property)
**Audience**: Interest-based — real estate investment, surf travel, expat life, tropical lifestyle
**Geo**: Australia, Singapore, USA, UK, Germany, Netherlands, Russia
**Budget**: $5-10/day
**Purpose**: Build video view audience for retargeting

### Template 2: Meta — Leads (Carousel)

**Objective**: OUTCOME_LEADS
**Format**: Carousel (multiple property photos, each card = different plot or angle)
**Audience**: Retarget video viewers (75%+ watched) + Lookalike of website visitors
**Geo**: Same as awareness
**Budget**: $10-20/day
**CTA**: "Learn More" → sumbawa.estate landing page
**Purpose**: Capture leads (name, email, WhatsApp)

### Template 3: Meta — Conversion (Lead Form)

**Objective**: OUTCOME_LEADS
**Format**: Single image + Instant Form (in-app lead capture)
**Audience**: Retarget website visitors (last 30 days) who didn't convert
**Form fields**: Name, Email, Phone, "What's your budget?", "When do you plan to invest?"
**Budget**: $10-15/day
**Purpose**: Direct lead capture without leaving Facebook

### Template 4: Google — Search Intent

**Type**: SEARCH
**Keywords** (Phrase Match):
- "sumbawa land for sale"
- "indonesia beachfront land"
- "sumbawa property investment"
- "surf land indonesia"
- "bali alternative investment"
**Negative keywords**: "rent", "hotel", "booking", "cheap flight"
**Geo**: Australia, Singapore, USA, UK
**Budget**: $15-30/day
**Bid strategy**: Maximize Conversions (after 30+ conversions) or Manual CPC (start)
**Purpose**: Capture high-intent search traffic

### Template 5: Google — Performance Max

**Type**: PERFORMANCE_MAX
**Assets**: Images (property, beach, surf) + Headlines + Descriptions + Videos
**Audience signals**: Real estate investors, surf enthusiasts, expat communities
**Budget**: $20-30/day
**Purpose**: Cross-network reach (Search, Display, YouTube, Gmail, Discover)

## Output

### Action Log

Every campaign action must be logged to `~/drafts/ad-cabinet/action-log.md`:

```markdown
## [YYYY-MM-DD HH:MM] — [Action Type]

- **Platform**: Meta / Google
- **Campaign**: [name]
- **Action**: Created / Paused / Budget changed / Creative updated / etc.
- **Details**: [what changed, old value → new value]
- **Reason**: [why this action was taken]
- **Status**: PAUSED / awaiting approval / ACTIVE
```

### Campaign Reports

Save performance summaries to `~/drafts/ad-cabinet/reports/YYYY-MM-DD.md`

## Workflow

### Creating a New Campaign

0. **Read `~/memory/runbook-campaign-launch.md`** — follow pre-launch checklist
1. **Read `~/memory/audiences.md`** and `~/memory/platform-rules.md` — apply Active Rules
2. Choose template from campaign-templates (or custom based on ad-spy insights)
3. Prepare creative assets (coordinate with creative-generator skill)
4. Define audience (from audiences.md or custom)
5. Create campaign via API — **ALWAYS PAUSED**
6. Log action to action-log.md
7. **Create `~/memory/campaigns/{SLUG}.md`** — per-campaign record (see runbook template)
8. **Update `~/memory/campaigns/campaign-log.md`** — add row to Active table
9. Notify ac1b: "Campaign [name] created and paused. Ready for review."
10. Wait for approval before activating

### Daily Check

1. Pull performance for all ACTIVE campaigns
2. Flag anomalies: spend > budget, CTR drop > 30%, CPL spike > 2x
3. Recommend actions: pause underperformers, scale winners
4. Update action-log.md

### Budget Optimization

- **Kill** ads with CPL > $50 after 72 hours
- **Scale** ads with CPL < $15 and ROAS > 2x (increase budget by 20%, max once per 3 days)
- **Rotate** creatives weekly to prevent fatigue
- **Never increase budget by more than 20% at once** (Meta penalizes big jumps)
