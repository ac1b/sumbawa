# Campaign Templates

Ready-to-use campaign structures. Pick a template, fill in creative assets, launch PAUSED.

---

## META-01: Awareness — Drone Video

```
Campaign:
  name: "Sumbawa Coast — Drone Tour [DATE]"
  objective: OUTCOME_AWARENESS
  special_ad_categories: ["HOUSING"]
  budget: $5-10/day (campaign budget optimization)

Ad Set:
  name: "Surf Investors — AU/US/UK"
  targeting:
    geo: AU, US, UK, SG
    interests: surfing, real estate investment
    placements: Instagram Reels, Facebook Feed, Instagram Feed
  optimization: ThruPlay (video views)

Ad:
  format: Video (15-30 sec drone footage)
  primary_text: "33km of untouched coastline. 15+ world-class surf breaks. Land from $10/sqm. West Sumbawa — before the world catches on."
  headline: "West Sumbawa — The Last Affordable Surf Coast"
  cta: LEARN_MORE
  link: https://sumbawa.estate
```

---

## META-02: Leads — Property Carousel

```
Campaign:
  name: "Sumbawa Plots — Carousel [DATE]"
  objective: OUTCOME_LEADS
  special_ad_categories: ["HOUSING"]
  budget: $10-20/day

Ad Set:
  name: "Retarget Video Viewers 75%+"
  targeting:
    custom_audience: video viewers (75%+ from META-01)
    OR: website visitors (last 30 days)
  optimization: Leads

Ad:
  format: Carousel (3-5 cards)
  cards:
    1: Beachfront Kertasari — 2,500 m², $45K ($18/sqm) [photo]
    2: Coastal Poto Tano — 10,000 m², $95K ($10/sqm) [photo]
    3: West Sumbawa Coast — 15+ surf breaks [drone shot]
    4: Kiantar Airport — under construction, 15 min from plots [aerial]
    5: "Compare: Bali $500-2000/sqm vs Sumbawa $10-18/sqm" [infographic]
  primary_text: "Two prime plots in West Sumbawa — the coast investors are watching. Beachfront from $10/sqm with new international airport under construction nearby."
  headline: "Secure Your Plot — West Sumbawa"
  cta: LEARN_MORE
  link: https://sumbawa.estate
```

---

## META-03: Conversion — Instant Lead Form

```
Campaign:
  name: "Sumbawa Leads — Form [DATE]"
  objective: OUTCOME_LEADS
  special_ad_categories: ["HOUSING"]
  budget: $10-15/day

Ad Set:
  name: "Website Retarget + Lookalike"
  targeting:
    custom_audience: website visitors (last 14 days) who did NOT convert
    OR: lookalike (1%) of form submitters
  optimization: Leads (instant form)

Ad:
  format: Single image (best performing property photo)
  primary_text: "Interested in West Sumbawa? Get the full investment brochure — plots, pricing, legal guide, and ROI projections."
  headline: "Free Sumbawa Investment Guide"
  cta: SIGN_UP

Lead Form:
  name: "Sumbawa Investment Inquiry"
  questions:
    - Full Name (prefilled)
    - Email (prefilled)
    - Phone Number
    - "What's your investment budget?" [dropdown: Under $25K / $25-50K / $50-100K / $100K+]
    - "When do you plan to invest?" [dropdown: 1-3 months / 3-6 months / 6-12 months / Just exploring]
  privacy_policy: https://sumbawa.estate/privacy
  thank_you:
    headline: "We'll be in touch within 24 hours"
    description: "Check your email for the investment guide. Questions? WhatsApp us."
    cta: Visit Website → https://sumbawa.estate
```

---

## GOOGLE-01: Search — Intent Keywords

```
Campaign:
  name: "Sumbawa Search — Intent [DATE]"
  type: SEARCH
  budget: $15-30/day
  bid_strategy: Manual CPC ($2-5 max CPC) → switch to Maximize Conversions after 30 conversions
  geo: Australia, Singapore, USA, UK, Germany
  languages: English

Ad Group 1: "Sumbawa Land"
  keywords (Phrase Match):
    - "sumbawa land"
    - "sumbawa property"
    - "sumbawa investment"
    - "west sumbawa land"
  negatives: rent, hotel, tour, flight, booking, job, volunteer

Ad Group 2: "Indonesia Land Investment"
  keywords (Phrase Match):
    - "indonesia beachfront land"
    - "indonesia land investment"
    - "indonesia property foreigners"
    - "bali alternative investment"
  negatives: same + "bali villa rent", "bali hotel"

Ad Group 3: "Surf Land"
  keywords (Phrase Match):
    - "surf land indonesia"
    - "surf property asia"
    - "beachfront land surf"

Responsive Search Ad:
  headlines (15):
    - "West Sumbawa — Beachfront Land"
    - "Land From $10/sqm"
    - "15+ Surf Breaks Nearby"
    - "New Airport Under Construction"
    - "Secure Your Plot Today"
    - "Indonesia's Next Investment Frontier"
    - "2,500 m² Beachfront — $45K"
    - "10,000 m² Coastal — $95K"
    - "Leasehold Options Available"
    - "Free Investment Guide"
    - "Bali Prices vs Sumbawa"
    - "Golden Visa Eligible"
    - "PT PMA Structure Available"
    - "West Sumbawa Coast"
    - "Surf & Invest in Sumbawa"
  descriptions (4):
    - "Premium beachfront & coastal plots in West Sumbawa. 33km of untouched coastline, 15+ world-class surf breaks. From $10/sqm."
    - "New Kiantar Airport 15 min away. Infrastructure boom driving land values. Secure your position before prices catch up."
    - "Full legal support for foreign investors. PT PMA, Hak Pakai, leasehold structures. Free consultation."
    - "Compare: Bali $500-2000/sqm vs West Sumbawa $10-18/sqm. Same island chain, 1/50th the price."
  final_url: https://sumbawa.estate
  path1: sumbawa
  path2: land
```

---

## GOOGLE-02: Performance Max

```
Campaign:
  name: "Sumbawa PMax [DATE]"
  type: PERFORMANCE_MAX
  budget: $20-30/day
  bid_strategy: Maximize Conversions
  geo: Australia, Singapore, USA, UK

Asset Group:
  name: "Sumbawa Land Investment"
  images: [5-10 property/coast/surf photos, different aspect ratios]
  videos: [1-2 drone videos, 15-30 sec]
  headlines (5): [reuse from GOOGLE-01]
  long_headlines (5):
    - "Premium Beachfront Land in West Sumbawa — Indonesia's Next Investment Frontier"
    - "From $10/sqm — World-Class Surf Coast With New International Airport"
    - "2,500 m² Beachfront Plot Near 15+ Surf Breaks for $45,000"
    - "Why Savvy Investors Are Looking Beyond Bali to West Sumbawa"
    - "Coastal Development Land — 10,000 m² Near New Kiantar Airport"
  descriptions (5): [reuse from GOOGLE-01]
  final_url: https://sumbawa.estate

Audience Signals:
  - Custom segment: searched for "indonesia land", "surf property", "bali investment"
  - In-market: Real estate, Travel SE Asia
  - Interests: Surfing, Property investment, Expat life
```
