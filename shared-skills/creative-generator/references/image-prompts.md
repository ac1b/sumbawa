# Image Generation Prompts

Tested prompts for Flux / SDXL models. Use via API (Replicate, ModelsLab, Pixazo).

## API Usage (curl)

```bash
# Replicate (Flux Schnell — fast, cheap)
curl -s -X POST "https://api.replicate.com/v1/predictions" \
  -H "Authorization: Bearer ${REPLICATE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "black-forest-labs/flux-schnell",
    "input": {
      "prompt": "[PROMPT HERE]",
      "aspect_ratio": "16:9",
      "num_outputs": 1
    }
  }'
```

Aspect ratios by placement:
- Feed (Meta/Google): 1:1 (1080x1080) or 4:5 (1080x1350)
- Stories/Reels: 9:16 (1080x1920)
- Google Display: 16:9 (1200x628)
- Carousel: 1:1 per card

---

## Property / Land Prompts

### Beachfront Plot
```
Aerial drone photograph of a pristine beachfront land plot in tropical Indonesia, turquoise ocean water, white sand beach, coconut palm trees bordering the property, lush green vegetation, golden hour sunlight, no buildings, undeveloped paradise, photorealistic, 8K quality
```

### Coastal Development Site
```
Wide angle aerial photo of a large coastal land plot in Southeast Asia, overlooking the ocean, gentle hillside with tropical vegetation, dirt road access, surrounding palm trees, clear blue sky, morning light, real estate photography style, photorealistic
```

### Surf Break View
```
Dramatic photograph of a world-class surf break in Indonesia, perfect barrel wave, tropical island coastline in background, palm-lined beach, early morning golden light, shot from elevated cliff viewpoint, professional surf photography, National Geographic style
```

## Lifestyle Prompts

### Surf Lifestyle
```
Professional photograph of a surfer walking along a pristine tropical beach in Indonesia at sunset, surfboard under arm, palm trees silhouette, golden light reflecting on wet sand, crystal clear water, no crowds, peaceful and aspirational, lifestyle photography
```

### Eco-Lodge Vision
```
Architectural visualization of a modern tropical eco-lodge with open-air design, natural wood and stone materials, infinity pool overlooking the ocean, tropical garden, sustainable architecture, Bali-style luxury meets modern minimalism, golden hour, photorealistic render
```

### Investment Lifestyle
```
Professional lifestyle photo of a couple standing on a tropical hilltop overlooking turquoise ocean coastline in Indonesia, casual elegant clothing, viewing a beautiful beachfront property site, feeling of freedom and possibility, warm natural lighting, aspirational
```

## Comparison / Infographic Style

### Price Map
```
Clean modern infographic-style aerial map showing Indonesian island chain, highlighting Bali (labeled "$1,500/sqm") and Sumbawa (labeled "$10/sqm"), ocean in beautiful turquoise, islands in green, minimalist design, white text labels, professional data visualization
```

### Before/After (Development)
```
Split-screen aerial photograph, left side showing undeveloped tropical beachfront land with palm trees, right side showing a tasteful small resort development on similar land, both in golden hour light, Indonesia tropical setting, showing potential transformation
```

## Seasonal / Topical

### Surf Season
```
Epic aerial photograph of multiple perfect surf waves breaking along a tropical Indonesian coastline, 5-6 surfers in the water, palm-lined coast, crystal clear turquoise water, drone perspective, professional surf magazine quality, dramatic composition
```

### Sunset Property
```
Stunning sunset photograph from a beachfront property in West Sumbawa Indonesia, silhouette of palm trees against orange and purple sky, calm ocean reflecting sunset colors, no buildings in frame, feeling of owning a private paradise, magazine quality
```

---

## Prompt Engineering Tips

1. **Always include**: "photorealistic", "professional photography", specific lighting ("golden hour", "morning light")
2. **Avoid**: "AI generated", "digital art", "illustration" — we want photo-real
3. **For consistency**: Add "West Sumbawa Indonesia" and "tropical" to every prompt
4. **Text in images**: Flux handles text well. Add "with text overlay: [YOUR TEXT]" to include text
5. **Negative prompts** (if model supports): "watermark, text, logo, people's faces closeup, stock photo, oversaturated, HDR, cartoon"
6. **Batch generation**: Generate 4-5 variants per prompt, pick the best
7. **Aspect ratio matters**: Always match the platform (1:1 for feed, 9:16 for stories)
