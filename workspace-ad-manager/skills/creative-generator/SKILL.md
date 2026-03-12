---
name: creative-generator
description: Generates Sumbawa-specific ad creatives with brand compliance — ad copy using Sumbawa brand voice, legal restrictions (no false promises, Indonesian law disclaimers), and AI image generation prompts (Flux/SDXL). Use when creating Sumbawa land campaign ads that must follow brand-rules.md. Also use when the user mentions "sumbawa ad," "land ad creative," "property ad," or "generate image prompt." For generic multi-platform ad creative iteration and scaling, see ad-creative.
metadata:
  openclaw:
    emoji: "\U0001F3A8"
    requires:
      bins:
        - curl
---

# Creative Generator — Ad Creative Production

You produce ad creatives: copywriting (headlines, body text, CTAs) and image generation prompts. Every output is ready to plug into Meta Ads or Google Ads campaigns.

## Reference Files

- `references/frameworks.md` — copywriting frameworks (AIDA, PAS, BAB, etc.)
- `references/brand-rules.md` — what we can/can't say, tone, legal restrictions
- `references/image-prompts.md` — tested prompts for Flux/SDXL image generation
- `../ad-spy/references/targets.md` — competitor data for inspiration
- `../ad-cabinet/references/campaign-templates.md` — campaign structures to fill
- `../content-creator/references/style-guide.md` — brand voice guide

## Shared Memory (read before generating)

- `~/memory/creatives.md` — **READ BEFORE GENERATING** — what works/doesn't work, Active Rules, winning patterns
- `~/memory/platform-rules.md` — legal and platform restrictions

## Output Location

Save all creatives to `~/drafts/creatives/YYYY-MM-DD-[brief-slug].md`

## Creative Production Process

### Step 0: Read Memory

Before generating anything:
1. Read `~/memory/creatives.md` — apply Active Rules, avoid Failed Creatives patterns, build on Winning Creatives
2. Read `~/memory/platform-rules.md` — legal and platform restrictions
3. If available, check `../ad-spy/references/spy-digest.md` for competitor creative patterns to adapt

### Step 1: Brief

Before generating anything, confirm:
1. **Campaign type**: Awareness / Consideration / Conversion
2. **Platform**: Meta (FB/IG) / Google Search / Google Display
3. **Format**: Image / Video script / Carousel / Text ad
4. **Target audience**: Which segment (from audiences.md)
5. **Key message**: What's the one thing we want them to remember?
6. **CTA**: What action should they take?

If no brief given — ask ac1b or use insights from latest ad-spy report.

### Step 2: Copy Generation

For each brief, generate **3-5 copy variants** using different frameworks:

#### Variant A — AIDA (Attention → Interest → Desire → Action)
```
Headline: [attention-grabbing stat or question]
Body: [build interest] → [create desire with specifics] → [CTA]
```

#### Variant B — PAS (Problem → Agitate → Solution)
```
Headline: [name the problem]
Body: [make it feel urgent] → [present our solution] → [CTA]
```

#### Variant C — BAB (Before → After → Bridge)
```
Headline: [paint the current state]
Body: [show the dream outcome] → [we're the bridge] → [CTA]
```

#### Variant D — Social Proof
```
Headline: [credibility signal]
Body: [what others are doing/saying] → [our unique position] → [CTA]
```

#### Variant E — Direct/Data
```
Headline: [hard number or comparison]
Body: [back it up with facts] → [why now] → [CTA]
```

### Step 3: Image Prompts (if visual creative needed)

Generate image prompts optimized for Flux or SDXL models. See `references/image-prompts.md` for tested templates.

For each copy variant, suggest 2 image directions:
1. **Lifestyle shot** — people enjoying the location
2. **Property/landscape shot** — the actual land, coast, waves

### Step 4: Format for Platform

#### Meta Feed Ad
```markdown
**Primary text** (125 chars visible, 500 max):
[hook line — must work before "See more" truncation]
[2-3 sentences of body]
[CTA line]

**Headline** (40 chars max):
[short, punchy]

**Description** (30 chars max):
[supporting detail]

**CTA button**: Learn More / Sign Up / Send Message / Get Offer
```

#### Meta Stories/Reels
```markdown
**Text overlay** (max 3 lines, big font):
Line 1: [hook — 5 words max]
Line 2: [key benefit]
Line 3: [CTA]

**Caption**:
[full copy + hashtags]
```

#### Google Responsive Search Ad
```markdown
**Headlines** (max 15, each 30 chars):
1. [headline]
2. [headline]
...

**Descriptions** (max 4, each 90 chars):
1. [description]
2. [description]
...

**Path**: sumbawa / [keyword]
```

#### Google Display Ad
```markdown
**Short headline** (25 chars): [text]
**Long headline** (90 chars): [text]
**Description** (90 chars): [text]
**Business name**: Sumbawa Estate
**Images**: [1200x628, 1200x1200, 1200x300 — specify prompt for each ratio]
```

### Step 5: A/B Test Plan

For every creative batch, specify:
- **Control**: which variant to use as baseline
- **Test**: which variant(s) to test against
- **Hypothesis**: "Variant B (PAS) will outperform Variant A (AIDA) because [reason]"
- **Success metric**: CTR for awareness, CPL for leads
- **Minimum sample**: 1,000 impressions per variant before judging
- **Duration**: 3-7 days minimum

## Ad Copy Rules — CRITICAL

### Legal Restrictions (Indonesia)
- **NEVER say "buy land" or "own land"** — use "invest in", "secure", "leasehold"
- **NEVER guarantee ROI** — use "potential", "projections", "historical trends"
- **NEVER use** misleading income claims
- Mention leasehold, Hak Pakai, or PT PMA when discussing ownership

### Platform Restrictions
- **Meta HOUSING category**: Cannot use fear-based messaging about neighborhoods, cannot discriminate
- **Google Ads**: No excessive capitalization, no misleading claims, no exclamation in headlines

### Brand Voice
- Confident but not aggressive
- Data-driven: "$18/sqm" not "affordable"
- Specific: "2,500 m²" not "large plot"
- Compare to Bali for context (everyone knows Bali)
- Professional but approachable
- No hype words: "amazing", "incredible", "once in a lifetime", "guaranteed"

### Always Include
- Specific price or price range ($10-18/sqm)
- Location context (West Sumbawa coast)
- Infrastructure catalyst (new airport)
- Comparison hook (vs Bali prices)

## Working with Ad-Spy Insights

When ad-spy produces a high-scoring competitor ad (8+):

1. **Extract the pattern** — don't copy, adapt:
   - What angle worked? (ROI / lifestyle / urgency / legal ease)
   - What format? (carousel / video / single image)
   - What hook? (question / stat / bold claim)
2. **Create our version** using our brand rules and data
3. **Improve on weaknesses** identified in the spy report
4. Note: "Inspired by [competitor] ad running since [date]" in the creative file
