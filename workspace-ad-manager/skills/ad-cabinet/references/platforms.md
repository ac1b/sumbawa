# Platform API Reference

## Meta Ads API

### Setup Requirements

1. **Meta Business Suite** account at business.facebook.com
2. **Facebook Page** for sumbawa.estate
3. **Instagram Business** account linked to FB Page
4. **Meta App** (developers.facebook.com) with `ads_management` permission
5. **Long-lived access token** (60 days, must be refreshed)

### Environment Variables

```
META_ADS_ACCESS_TOKEN=   # Long-lived user access token
META_AD_ACCOUNT_ID=      # Without "act_" prefix (just the number)
META_PAGE_ID=            # Facebook Page ID
META_PIXEL_ID=           # Meta Pixel ID for tracking
```

### Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/act_{id}/campaigns` | GET | List campaigns |
| `/act_{id}/campaigns` | POST | Create campaign |
| `/{campaign_id}` | POST | Update campaign |
| `/{campaign_id}/adsets` | GET/POST | Manage ad sets |
| `/{adset_id}/ads` | GET/POST | Manage ads |
| `/{campaign_id}/insights` | GET | Performance data |
| `/act_{id}/customaudiences` | GET/POST | Manage audiences |
| `/act_{id}/adimages` | POST | Upload images |
| `/act_{id}/advideos` | POST | Upload videos |

### Token Refresh

Long-lived tokens expire in 60 days. Refresh before expiry:

```bash
curl -s "https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=${META_APP_ID}&client_secret=${META_APP_SECRET}&fb_exchange_token=${META_ADS_ACCESS_TOKEN}"
```

### Rate Limits

- Business tier: ~200 calls per hour per ad account
- Insights: max 600 calls per 5 minutes
- Batch API available for bulk operations (up to 50 requests per batch)

### Special Ad Category

**MANDATORY for real estate.** Must be set at campaign level:
```json
"special_ad_categories": ["HOUSING"]
```

Restrictions when HOUSING is active:
- No age targeting
- No gender targeting
- No zip/postal code targeting
- Minimum 15-mile radius for location targeting
- No exclusion of multicultural affinity segments

---

## Google Ads API

### Setup Requirements

1. **Google Ads account** at ads.google.com
2. **MCC (Manager) account** for API access
3. **Google Cloud Project** with Google Ads API enabled
4. **OAuth2 credentials** (client ID + secret)
5. **Developer token** (apply through MCC, basic access ~1 week)

### Environment Variables

```
GOOGLE_ADS_CLIENT_ID=        # OAuth2 client ID
GOOGLE_ADS_CLIENT_SECRET=    # OAuth2 client secret
GOOGLE_ADS_REFRESH_TOKEN=    # OAuth2 refresh token
GOOGLE_ADS_DEVELOPER_TOKEN=  # API developer token
GOOGLE_ADS_CUSTOMER_ID=      # Account ID (no dashes)
GOOGLE_ADS_LOGIN_CUSTOMER_ID= # MCC account ID (if using MCC)
```

### GAQL (Google Ads Query Language)

Used for all read operations. SQL-like syntax:

```sql
-- Campaign performance
SELECT campaign.name, campaign.status,
       metrics.impressions, metrics.clicks, metrics.ctr,
       metrics.cost_micros, metrics.conversions,
       metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC

-- Ad group keywords
SELECT ad_group.name, ad_group_criterion.keyword.text,
       ad_group_criterion.keyword.match_type,
       metrics.impressions, metrics.clicks
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS

-- Search terms report
SELECT search_term_view.search_term,
       metrics.impressions, metrics.clicks, metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_7_DAYS
ORDER BY metrics.impressions DESC
```

### Rate Limits

- 15,000 requests per day (basic access)
- 1,000 operations per mutate request
- GAQL queries: 1,000 per day per customer ID

---

## Pixel / Conversion Tracking

### Meta Pixel

Install on sumbawa.estate for tracking:
- PageView (all pages)
- ViewContent (property pages)
- Lead (form submission)
- Contact (WhatsApp click)

### Google Ads Conversion Tracking

- Global site tag on all pages
- Conversion actions: Form submission, WhatsApp click, Phone call
- Enhanced conversions with first-party data (email, phone)
