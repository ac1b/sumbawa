# Memory — Sumbawa OpenClaw

## Проект
- OpenClaw AI agent для продажи земли в **West Sumbawa** (Индонезия)
- Путь: `/root/sumbawa-openclaw/`
- Статический сайт: `/root/sumbawa-land/`
- Владелец: ac1b (@detroitty, Telegram ID 802940343)
- Домен: sumbawa.estate (не куплен), сайт: http://178.16.140.84/sumbawa/

## Инфраструктура
- **Контейнеры:** `sumbawa-agent` (node:22-bookworm) + `sumbawa-scraper` (Python + Scrapling + Chromium)
- **docker-compose v1** (баг ContainerConfig: `docker rm -f` + `docker-compose up -d`)
- **Telegram бот:** @sumbawa1_bot
- **OpenClaw:** 2026.3.1 → можно обновить
- **Gateway:** порт 18789 (mapped 19000)
- **Volumes:** agent-home, npm-global, npm-bin (persistent)
- **Scraper API:** `http://scraper:8100` — POST /fetch (stealth/fast), POST /search (Meta), GET /health

## Агенты (5, все MiniMax M2.5 Highspeed)

| Агент | Роль | Скиллы | tools.allow |
|-------|------|--------|-------------|
| **Petu** (sumbawa) | Диспетчер + продажи | 10 скилов | full |
| **content-writer** | Контент | 10 скилов | read,write,edit,web_search,web_fetch,exec |
| **competitor-spy** | Конкуренты | 2 скила | full |
| **ad-manager** | Реклама | 6 скилов | read,write,edit,exec (deny: web_search) |
| **analytics-brain** | Аналитика | 4 скила | read,write,edit,exec (deny: web_search) |

### Архитектурные правила
- Petu НЕ делает работу субагентов — только делегирует через exec()
- Только ad-manager делает POST к Meta API, analytics-brain только GET
- Retry-лимит: макс 3 попытки, потом СТОП
- 32 скила всего в workspace/skills/

## MiniMax Config (КРИТИЧНО)
- `baseUrl: "https://api.minimax.io/anthropic"` (НЕ /v1)
- `api: "anthropic-messages"` (НЕ openai-completions)
- `reasoning: true`, `contextWindow: 200000`, `timeoutSeconds: 300`
- `maxSpawnDepth: 2, maxChildrenPerAgent: 3`

### MiniMax 404 bug (fixed)
- auto-generated `agents/*/agent/models.json` с `baseUrl: "/v1"` (wrong)
- Fix: docker-compose entrypoint патчит models.json

### MiniMax поведенческие проблемы
- Сдаётся при первой сложности ИЛИ долбит API бесконечно
- Решения: paired examples (OK/BAD), ПОЧЕМУ к запретам, таблицы зон, язык: русский для ac1b / английский для клиентов

## Bug #10386 — Skills не загружаются у субагентов
- Gateway не инжектит workspace скилы в system prompt для non-default агентов
- **Workaround:** AGENTS.md с таблицей скилов + пути к SKILL.md, агент читает через read tool
- Применён ко всем 5 агентам

## Участки (2 шт)
1. **Beachfront, Kertasari** — 2,500 m², $45K, $18/sqm
2. **Coastal, Poto Tano** — 10,000 m² (1 ha), $95K, $10/sqm
- **ONLY West Sumbawa.** Never mention East Sumbawa.

## Google Ads — настроен (2026-03-06)
- Test MCC: Claw Test (2022414180)
- Test Client: Sumbawa Test Client (2208945093), IDR, Makassar
- Dev token: test-only, для прода — Basic Access
- API v20: `login-customer-id` header, `containsEuPoliticalAdvertising: 3`, `"manualCpc": {}`
- OAuth refresh token — истекает через ~7 дней

## Pipeline — работает (2026-03-06)
```
User → PETU → competitor-spy (research) → PETU → ad-manager (create campaign)
```
- Тестовые кампании: `Sumbawa Land - Test Search`, `Sumbawa Land - Main Search`
- ad-manager 40 retries bug → добавлены mutate-примеры в SKILL.md
- PETU пропускал research → добавлен multi-step в IDENTITY.md

## Credentials (.env)
- MINIMAX_API_KEY, ANTHROPIC_API_KEY (кредиты кончились), BRAVE_SEARCH_API_KEY
- TELEGRAM_BOT_TOKEN, META_ADS_ACCESS_TOKEN, META_AD_ACCOUNT_ID (sandbox)
- GOOGLE_ADS_LOGIN_CUSTOMER_ID

## pSEO (sumbawa-land)
- 615 HTML страниц, 5 языков (EN/DE/RU/JA/ZH)
- `taxonomy.py → ai_fill.py (MiniMax) → JSON → generate.py (Jinja2) → /var/www/sumbawa/`
- Подробности: `/root/sumbawa-land/PLAYBOOK.md`

## TODO
- [ ] Doctor warning: groupPolicy=allowlist, пустой allowFrom
- [ ] META_PAGE_ID, META_PIXEL_ID — не заданы
- [ ] Google Ads Basic Access — подать заявку
- [ ] Refresh token renewal
- [ ] Тест analytics-brain на Google Ads данных
- [ ] DNS sumbawa-land.com → сервер
