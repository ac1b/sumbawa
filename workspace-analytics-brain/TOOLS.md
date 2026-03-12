# TOOLS.md - Analytics Brain Tools

## Meta Ads API (GET/read-only)
- Base URL: https://graph.facebook.com/v21.0
- Account: act_${META_AD_ACCOUNT_ID}
- Token: $META_ADS_ACCESS_TOKEN
- All operations via exec + curl
- **GET requests ONLY.** POST/PUT/DELETE → that's ad-manager's job

## Useful Endpoints
```bash
# Account insights (today)
curl -s "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/insights?fields=impressions,clicks,ctr,spend,actions&date_preset=today&access_token=${META_ADS_ACCESS_TOKEN}"

# Campaign breakdown (last 7 days)
curl -s "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/insights?fields=campaign_name,impressions,clicks,ctr,spend,actions&date_preset=last_7d&time_increment=1&access_token=${META_ADS_ACCESS_TOKEN}"

# Active campaigns list
curl -s "https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/campaigns?fields=name,status,objective&effective_status=['ACTIVE']&access_token=${META_ADS_ACCESS_TOKEN}"
```

## RETRY LIMIT
- Maximum 3 attempts per endpoint
- 401/403 → token expired, STOP
- 429 → wait, retry
- After 3 failures → STOP, report

## Results
All reports go to `~/drafts/analytics/`:
- `daily/YYYY-MM-DD.md` — daily report
- `weekly/YYYY-MM-DD.md` — weekly report

## Google Ads API (GET/read-only via GAQL)
- Base URL: https://googleads.googleapis.com/v20
- Customer ID: ${GOOGLE_ADS_CUSTOMER_ID}
- Login Customer ID (MCC): ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}

### OAuth Token Refresh (REQUIRED before every request)
```bash
ACCESS_TOKEN=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "client_id=${GOOGLE_ADS_CLIENT_ID}" \
  -d "client_secret=${GOOGLE_ADS_CLIENT_SECRET}" \
  -d "refresh_token=${GOOGLE_ADS_REFRESH_TOKEN}" \
  -d "grant_type=refresh_token" | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
```

### GAQL Query (searchStream)
```bash
curl -s -X POST "https://googleads.googleapis.com/v20/customers/${GOOGLE_ADS_CUSTOMER_ID}/googleAds:searchStream" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT campaign.name, metrics.impressions, metrics.clicks, metrics.cost_micros FROM campaign WHERE segments.date DURING LAST_7_DAYS"}'
```

### Important Headers (every request)
- `Authorization: Bearer $ACCESS_TOKEN`
- `developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}`
- `login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}`

### Known Quirks
- Budget/cost values are in micros (divide by 1,000,000 for USD)
- `login-customer-id` MANDATORY even for direct access
