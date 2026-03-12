# Sumbawa Advertising System — Research & Architecture

_Date: 2026-03-04_

## Текущее состояние

5 скиллов: `sumbawa-sales`, `content-creator`, `seo-optimizer`, `lead-qualifier`, `follow-up`
2 агента: `sumbawa` (MiniMax), `content-writer` (Claude)
Каналы: Telegram (@sumbawa1_bot)

## Целевая архитектура

### Новые агенты

```
ad-manager       — управление рекламными кабинетами Meta/Google
competitor-spy   — разведка конкурентов, сбор лучших практик
analytics-brain  — аналитика, самообучение, оптимизация
```

### Новые скиллы

1. `ad-cabinet` — создание/управление кампаниями через API
2. `ad-spy` — сбор рекламы конкурентов (Meta Ad Library, Google Transparency)
3. `creative-generator` — генерация креативов (текст + изображения)
4. `ad-analytics` — аналитика, отчёты, self-learning loop
5. `retargeting-funnel` — воронка ретаргетинга

### Поток данных

```
competitor-spy → ad-spy → "лучшие практики"
    ↓
content-writer → creative-generator → "креативы готовы"
    ↓
ad-manager → ad-cabinet → Meta/Google API → "кампании запущены"
    ↓
analytics-brain → ad-analytics → "CTR упал / ROAS вырос"
    ↓
    → creative-generator (новые креативы)
    → ad-manager (пауза/ротация/масштабирование)
```

---

## Инструменты и API

### Рекламные платформы

| Платформа | SDK/API | Стоимость |
|-----------|---------|-----------|
| Meta Ads | `facebook-nodejs-business-sdk` (npm) | Бесплатно (оплата ad spend) |
| Google Ads | `google-ads-api` (npm, Opteo) | Бесплатно (оплата ad spend) |

**Meta Marketing API** — полный контроль: создание кампаний, аудитории, бюджеты, креативы, отчёты.
- Advantage+ обязателен с Q1 2026 (legacy API deprecated)
- Special Ad Category: HOUSING — ограничения таргетинга (нет age/gender/zip)
- Node.js SDK: `facebook-nodejs-business-sdk`

**Google Ads API** — search, display, YouTube, Performance Max.
- Ежемесячные релизы с Jan 2026 (v23+)
- AI Max for Search — AI находит аудитории
- Google выпустил open-source MCP server для Ads API (Oct 2025)
- Node.js: `google-ads-api` (Opteo)

### Шпионаж за конкурентами

| Инструмент | Тип | Цена | API |
|-----------|-----|------|-----|
| Meta Ad Library (через Apify) | Cloud scraper | $5-25/run | REST |
| ScrapeCreators API | API service | Paid | REST |
| Google Transparency (GitHub scraper) | Open-source | Free | - |
| SerpApi | API service | From $50/mo | REST |
| AdSpy | SaaS | $149/mo (flat) | Включён |
| BigSpy | SaaS | $9-249/mo | Enterprise |

**Рекомендация**: Start free — Apify для Meta + GitHub scraper для Google. Если нужно больше → AdSpy $149/mo.

### Генерация креативов

**Изображения:**
| Модель | API провайдер | Цена |
|--------|--------------|------|
| Flux.1.1 Pro / Flux.2 | Replicate, ModelsLab, Pixazo | ~$0.01-0.05/image |
| SDXL | ModelsLab, Pixazo | ~$0.01/image |
| Pixazo API (beta) | pixazo.ai | Бесплатно (beta) |

- Можно fine-tune LoRA на фотографиях Sumbawa (5+ фото достаточно)
- ComfyUI для batch generation pipelines

**Текст (копирайт):**
- Claude/GPT-4 API — лучшее качество, multilingual
- Фреймворки: AIDA, PAS, Before/After/Bridge

**Видео:**
- FFmpeg + Node.js (бесплатно) — slideshow из Flux-картинок + drone footage
- Runway ML — text/image to video (платно)

### Автоматизация / Оркестрация

| Инструмент | Тип | Цена |
|-----------|-----|------|
| n8n (self-hosted) | Workflow automation | Free |
| Custom Node.js scheduler | Code | Free |

n8n готовые шаблоны:
- Meta Ads Creative Testing Workflow
- Upload Ads to Meta from Google Sheets/Drive
- AI Marketing Report (Google + Meta → Telegram)

### Самооптимизация

| Инструмент | Тип | Цена |
|-----------|-----|------|
| Meta Advantage+ | Built-in | Free |
| Meta Ax | Open-source Bayesian optimization | Free |
| Custom rules engine | Node.js | Free |

Логика rules engine:
1. Kill ads с CPL > $X после N часов
2. Scale бюджет на ads с ROAS > Y
3. Rotate креативы еженедельно
4. A/B test copy variants
5. Еженедельно: scrape конкурентов → анализ → feed в creative engine
6. Ежемесячно: adjust targeting по accumulated data

---

## OpenClaw скиллы из экосистемы

### Готовые к установке

1. **Adspirer Ads Agent** (`amekala/adspirer-ads-agent`)
   - 100+ tools через MCP: Google (39), Meta (20), LinkedIn (28), TikTok (4)
   - `openclaw plugins install openclaw-adspirer`
   - Free: 15 calls/mo, Pro: $99/mo (600 calls)

2. **Marketing Mode** (`thesethrose/marketing-mode`)
   - 23 дисциплины, 140+ стратегий
   - `openclaw skills install marketing-mode`

3. **7 Paid Media Skills** (`irinabuht12-oss/marketing-skills`)
   - Performance Auditor, Bid/Budget Manager, Creative Analyst
   - Audience Architect, Pacing Monitor, Cross-Platform Comparator, Weekly Report

4. **meta-ads-report** — мониторинг Meta Ads через чат
5. **cold-outreach** — email/SMS/LinkedIn DM
6. **social-media-lead-generation** — лидогенерация из соцсетей
7. **sovereign-brand-voice-writer** — контент в голосе бренда

---

## Пререквизиты для старта

1. **Meta Business Suite** — аккаунт + Facebook Page для sumbawa.estate
2. **Meta Ads Manager** — рекламный кабинет
3. **Instagram Business** — подключить к FB Page
4. **Google Ads account** — для search кампаний
5. **Adspirer account** (опционально) — MCP интеграция
6. **Flux API key** (Pixazo/ModelsLab) — генерация креативов

### Бюджеты

- Meta Ads: от $5/day тест ($150/mo)
- Google Ads: от $10/day тест ($300/mo)
- Инструменты: $0-150/mo
- **Минимум для запуска: $0 (кроме ad spend)**
- **Рекомендуемый тест: $500/mo ad spend**

---

## Real Estate специфика

1. **Special Ad Category HOUSING** — обязательно для Meta, ограничивает таргетинг
2. **Никогда не говорить "buy land"** — только "invest", "secure", "leasehold"
3. **Visual-first** — carousel, video, drone footage конвертят лучше всего
4. **Retargeting funnel**: Awareness (video) → Consideration (carousel) → Conversion (lead form/WhatsApp)
5. **Multilingual**: EN primary, возможно RU для русскоязычного рынка
6. **Low competition**: Sumbawa keywords имеют низкую конкуренцию в Google
7. **Средний CPL для real estate**: $20-50 (может быть ниже для niche market)
