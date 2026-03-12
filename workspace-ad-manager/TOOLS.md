# TOOLS.md - Ad Manager Tools

## Scraper API
- Health: curl -s http://scraper:8100/health
- Fetch: curl -s -X POST http://scraper:8100/fetch -H "Content-Type: application/json" -d "{\"url\":\"...\",\"stealth\":false}"
- Meta search: curl -s -X POST http://scraper:8100/search -H "Content-Type: application/json" -d "{\"search_terms\":\"...\",\"country\":\"ID\"}"

## Meta Ads API
- Base URL: https://graph.facebook.com/v21.0
- Account: act_${META_AD_ACCOUNT_ID}
- Token: $META_ADS_ACCESS_TOKEN
- All operations via exec + curl

## API RETRY LIMIT (MANDATORY)

### Rule:
1. Sent a request → got an error
2. **READ the error completely.** What exactly is wrong?
3. Fix the SPECIFIC parameter (not randomly)
4. Try again
5. Maximum **3 attempts per one endpoint**
6. After 3 — **STOP, report the error**

### Common Meta API errors:
| Code | Cause | What to do |
|------|-------|-----------|
| 400 | Invalid parameters | Read error.message, fix the specific parameter |
| 100 | Missing/invalid parameter | Check required fields in SKILL.md |
| 190 | Invalid access token | STOP. Token expired. Report |
| 294 | Quota exceeded | STOP. Wait. Report |
| 2635 | Special ad category required | Add special_ad_categories=["HOUSING"] |

### FORBIDDEN:
- Retry 5+ times in a row
- Change parameters randomly (daily_budget → lifetime_budget → bid_strategy)
- Ignore error text
- Create the same campaign multiple times

## Action Log
After EACH API call, write to `~/drafts/ad-cabinet/action-log.md`.
Before EACH task, read action-log — the work may already be done.

## Rules
- Scraper WORKS, do not say it doesn't
- If Google blocks (429) — use DuckDuckGo
- If there's no API token — say EXACTLY which one is needed

## Google Ads API
- Base URL: https://googleads.googleapis.com/v20
- Customer ID: ${GOOGLE_ADS_CUSTOMER_ID}
- Login Customer ID (MCC): ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}
- Developer Token: ${GOOGLE_ADS_DEVELOPER_TOKEN}

### OAuth Token Refresh (REQUIRED before every request)
```bash
ACCESS_TOKEN=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "client_id=${GOOGLE_ADS_CLIENT_ID}" \
  -d "client_secret=${GOOGLE_ADS_CLIENT_SECRET}" \
  -d "refresh_token=${GOOGLE_ADS_REFRESH_TOKEN}" \
  -d "grant_type=refresh_token" | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
```

### IMPORTANT Headers (every request)
- `Authorization: Bearer $ACCESS_TOKEN`
- `developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}`
- `login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}`

### Create Campaign (mutate)
See ad-cabinet SKILL.md for full curl examples with `containsEuPoliticalAdvertising: 3` and `manualCpc: {}` required fields.

### Known Quirks
- Test dev token: only works with test MCC accounts
- `login-customer-id` header is MANDATORY
- Budget amounts are in micros (1 USD = 1,000,000 micros)
