# Sumbawa OpenClaw — Архитектура и настройка агентов

## Как OpenClaw собирает промпт для модели

### System prompt structure (сверху вниз)

```
1. Core instructions (hardcoded OpenClaw)
   ├── Tool list с описаниями (read, write, exec, web_search...)
   ├── Reply tags / formatting rules
   ├── Messaging rules
   └── Reasoning tag hint (<think> если нужен)

2. Skills section (mandatory)
   ├── "Before replying: scan <available_skills>"
   ├── "If exactly one skill applies → read its SKILL.md, follow it"
   ├── <available_skills>
   │     <skill><name>sumbawa-sales</name>
   │       <description>...</description>
   │       <location>~/.openclaw/workspace/skills/sumbawa-sales/SKILL.md</location>
   │     </skill>
   │     ... (все скиллы агента, фильтруются через config skills:[])
   └── </available_skills>

3. Project Context (workspace files — грузятся ЦЕЛИКОМ)
   ├── ## AGENTS.md   — operating instructions
   ├── ## SOUL.md     — identity/persona ("embody its persona and tone")
   ├── ## TOOLS.md    — tool usage notes
   ├── ## IDENTITY.md — who am I
   ├── ## USER.md     — who am I helping
   └── ## HEARTBEAT.md

4. Silent Replies / Heartbeats rules
5. Runtime info (agent=sumbawa, model=MiniMax-M2.5, channel=telegram...)
```

### Ключевые механизмы

**Skill injection:** Скиллы из `skills:[]` конфига попадают в `<available_skills>` блок в system prompt. ~97 chars per skill (~25 токенов). Модель обязана сканировать descriptions перед каждым ответом.

**Skill loading:** Модель САМА решает прочитать SKILL.md через tool call `read`. OpenClaw не загружает SKILL.md автоматически — только description и path. Но внутри SKILL.md могут быть curl-примеры, и модель начинает их копировать.

**Workspace files:** ВСЕ .md файлы из workspace грузятся ЦЕЛИКОМ в system prompt как `## filename\n\ncontent`. Это 3000-5000 токенов overhead на каждый вызов.

**Tool execution:** OpenClaw даёт модели tool `exec` без ограничений на количество вызовов. Модель сама решает когда остановиться. Нет built-in retry лимита.

**Session persistence:** Каждый агент хранит session в `.jsonl` файле. При idle reset (1440 min) сессия сбрасывается.

---

## Проблемы MiniMax M2.5 в OpenClaw

### Почему тупит

1. **Копирует curl из SKILL.md буквально.** Видит `curl -s -X POST graph.facebook.com...` в SKILL.md → выполняет. Не понимает контекст "это пример, не инструкция".

2. **Нет retry-самоконтроля.** Получает ошибку → меняет один параметр наугад → retry. Повторяет 14 раз. Не анализирует текст ошибки.

3. **Дублирует работу другого агента.** Petu и ad-manager оба видели ad-cabinet SKILL.md → оба пошли создавать кампанию → 52 API вызова, результат ноль.

4. **Verbose.** Генерирует 56M токенов в бенчмарках vs 15M среднее. Тратит output на объяснения вместо действий.

5. **Стопорится на ~100 steps.** Может остановиться посреди задачи и ждать input.

6. **Сдаётся при первой сложности.** Говорит "инструмент не работает" без попытки, или спрашивает "с каких сайтов?" когда данные в reference-файлах.

### Сильные стороны (почему используем)

- **BFCL tool calling: 76.8%** — бьёт Claude Opus на 13.5 пунктов
- **SWE-Bench: 80.2%** — на уровне Opus
- **Стоимость: 1/20 от Opus** — $0.15 vs $3.00 per task
- **Скорость: 100 TPS Lightning** — 3x быстрее Opus
- **Бесплатный API tier** для наших объёмов

---

## Что сделано (v2, 2026-03-05)

### Архитектура агентов — строгое разделение

```
PETU (dispatcher + sales) — sumbawa-sales, lead-qualifier, follow-up
├── НЕ делает контент, НЕ сканирует конкурентов, НЕ трогает Meta API
├── Только делегирует через exec("openclaw agent --agent <name> --message ...")
│
├── CONTENT-WRITER — content-creator, seo-optimizer
│   └── Пишет посты, статьи, SEO. НЕ трогает API, НЕ сканирует конкурентов
│
├── COMPETITOR-SPY — ad-spy
│   └── Сканирует конкурентов, цены, SEO. НЕ создаёт кампании, НЕ пишет контент
│
├── AD-MANAGER — ad-cabinet, creative-generator, retargeting-funnel
│   └── ЕДИНСТВЕННЫЙ кто делает POST к graph.facebook.com. Action-log обязателен
│
└── ANALYTICS-BRAIN — ad-analytics
    └── Только GET запросы к Meta API (insights/read). НЕ создаёт/меняет кампании
```

### Config changes (openclaw.json)

- `sumbawa.skills: ["sumbawa-sales", "lead-qualifier", "follow-up"]` — было: no filter (все 12 скиллов)
- `analytics-brain.skills: ["ad-analytics"]` — было: ["ad-analytics", "retargeting-funnel"]
- `competitor-spy.workspace: "/root/.openclaw/workspace-competitor-spy"` — было: shared
- `analytics-brain.workspace: "/root/.openclaw/workspace-analytics-brain"` — было: нет

### Workspace files (что прописано в каждом)

Каждый агент имеет SOUL.md, IDENTITY.md, TOOLS.md с:
- **Зона ответственности** — что делает, что НЕ делает
- **Таблица "другие агенты"** — кто что делает, чтобы не дублировать
- **Retry-лимит** — макс 3 попытки, обязательный анализ ошибки перед retry
- **Конкретные маршруты действий** — пошаговые инструкции для типовых задач
- **Запреты** — graph.facebook.com только для ad-manager, POST только для ad-manager
- **Action-log** — ad-manager пишет в ~/drafts/ad-cabinet/action-log.md после каждого API вызова

### Docker (docker-compose.yml)

Все workspace bind-mounted:
```yaml
- ./workspace:/root/.openclaw/workspace
- ./workspace-ad-manager:/root/.openclaw/workspace-ad-manager
- ./workspace-content-writer:/root/.openclaw/workspace-content-writer
- ./workspace-competitor-spy:/root/.openclaw/workspace-competitor-spy
- ./workspace-analytics-brain:/root/.openclaw/workspace-analytics-brain
```

---

## Google Ads API (v20)

- **Test MCC**: Claw Test (2022414180)
- **Test Client**: Sumbawa Test Client (2208945093), IDR, Asia/Makassar
- **Dev token**: test-only (works only with test accounts)
- **Required headers**: `login-customer-id: ${GOOGLE_ADS_LOGIN_CUSTOMER_ID}` on EVERY request
- **Campaign creation**: must include `"containsEuPoliticalAdvertising": 3` and `"manualCpc": {}` for bid strategy
- **For production**: apply for Basic Access at ads.google.com/aw/apicenter (then can use real MCC 5423933395)
- **Refresh token**: expires in ~7 days, needs renewal

## Environment Variables Status (2026-03-06)

### Active
| Var | Status |
|-----|--------|
| `MINIMAX_API_KEY` | OK |
| `OPENCLAW_GATEWAY_TOKEN` | OK |
| `BRAVE_SEARCH_API_KEY` | OK |
| `TELEGRAM_BOT_TOKEN` | OK (@sumbawa1_bot) |
| `ANTHROPIC_API_KEY` | OK |
| `META_ADS_ACCESS_TOKEN` | OK |
| `META_AD_ACCOUNT_ID` | OK (1264146302479755) |
| `GOOGLE_ADS_CLIENT_ID` | OK |
| `GOOGLE_ADS_CLIENT_SECRET` | OK |
| `GOOGLE_ADS_REFRESH_TOKEN` | OK |
| `GOOGLE_ADS_DEVELOPER_TOKEN` | OK (test-only) |
| `GOOGLE_ADS_CUSTOMER_ID` | OK (2208945093 — test client) |
| `GOOGLE_ADS_LOGIN_CUSTOMER_ID` | OK (2022414180 — test MCC) |

### Not Set (needed later)
| Var | Purpose |
|-----|---------|
| `META_PAGE_ID` | Facebook Page (retargeting) |
| `META_PIXEL_ID` | Meta Pixel (tracking) |
| `META_APP_ID` | Token refresh |
| `META_APP_SECRET` | Token refresh |
| `REPLICATE_API_TOKEN` | AI image generation |

## Pipeline (end-to-end)

```
1. RESEARCH        competitor-spy → scan competitors, ads, pricing
                   Output: ~/drafts/ad-spy/, ~/memory/competitors.md

2. CONTENT         content-writer → SEO articles + 8-10 social posts
                   Input: competitors.md, content-strategy, style-guide
                   Output: ~/drafts/YYYY-MM-DD-topic.md

3. CREATIVE        ad-manager (creative-generator) → ad copy + image prompts
                   Input: competitors.md, creatives.md, learnings.md
                   Output: 3-5 variants (AIDA, PAS, BAB, Social Proof, Direct)

4. CAMPAIGN        ad-manager (ad-cabinet) → create campaigns via API
                   Input: runbook-campaign-launch.md, audiences.md, platform-rules.md
                   Output: PAUSED campaign → action-log.md → notify ac1b
                   Rule: ALL campaigns PAUSED. ac1b approves before live.

5. FUNNEL          ad-manager (retargeting-funnel) → 3-stage funnel
                   Stage 1 (40%): Awareness — video, reach
                   Stage 2 (35%): Consideration — retarget video viewers
                   Stage 3 (25%): Conversion — retarget site visitors, lead forms

6. MONITORING      analytics-brain → daily check + weekly deep dive
                   Input: Meta + Google metrics (GET only)
                   Output: ~/drafts/analytics/
                   Updates: audiences.md, creatives.md, learnings.md

7. LEADS           PETU → qualify leads (Hot/Warm/Cold)
                   Hot: notify ac1b. Follow-up: Day 2/5/10/20 (needs WhatsApp)

FEEDBACK LOOP:
  analytics → learnings.md → next creative batch
  competitor intel → winning patterns → new campaigns
```

## Что ещё можно сделать (TODO)

### DONE (2026-03-05)

1. ~~**Объяснять ПОЧЕМУ запрещено**~~ → добавлено в ad-manager SOUL.md
2. ~~**Paired examples (good + bad)**~~ → добавлено в Petu SOUL.md и ad-manager SOUL.md
3. ~~**Tool restrictions**~~ → tools.allow/deny для ad-manager, analytics-brain, content-writer
4. ~~**Увеличить timeoutSeconds**~~ → 300s в defaults
5. ~~**Workspace для ad-manager и content-writer**~~ → добавлено в openclaw.json
6. ~~**MiniMax provider fix**~~ → baseUrl → /anthropic, api → anthropic-messages, reasoning → true, contextWindow → 200000
7. ~~**Gateway bind**~~ → loopback (было lan)
8. ~~**Content-writer TOOLS.md**~~ → заменён boilerplate на реальные инструменты
9. ~~**Content-writer reference paths**~~ → исправлены на workspace/skills/
10. ~~**Дублирование правил Petu SOUL.md/IDENTITY.md**~~ → убрано, single source of truth
11. ~~**Противоречие в Petu**~~ → "не делай без просьбы" vs "просто делай" → разделено: для клиентов по скрипту, для ac1b сразу выполняй
12. ~~**maxSpawnDepth/maxChildrenPerAgent**~~ → 2/3 для защиты от runaway

### Осталось

1. **Few-shot в conversation history.**
   Вставить 2-3 "правильных" диалога user→agent в начало сессии через sessions API.

2. **Per-agent model routing.**
   Claude Sonnet/Opus для Petu (orchestrator), MiniMax для workers. Требует кредиты Anthropic.
   ```json
   {"id": "sumbawa", "model": {"primary": "anthropic/claude-sonnet-4-6"}}
   ```

3. **Action-log для всех агентов.**
   Сейчас только ad-manager. Добавить для competitor-spy и content-writer.

4. **Sandbox mode для ad-manager.**
   ```json
   {"id": "ad-manager", "sandbox": {"mode": "all"}}
   ```
   Может сломать доступ к workspace/skills — нужно тестировать.

5. **Мониторинг API вызовов.**
   Считать exec calls к graph.facebook.com в session .jsonl. Алерт если > 10.

6. **Session token monitoring.**
   inputTokens/outputTokens в sessions.json. MiniMax verbose — следить за расходом.

---

## Ключевые файлы

```
/root/sumbawa-openclaw/
├── ARCHITECTURE.md              ← этот файл
├── .env                          # credentials
├── docker-compose.yml            # all workspaces bind-mounted
├── config/openclaw.json          # agent config, skills filter, workspaces
├── workspace/                    # Petu (10 skills: sales, qualifier, follow-up, product-marketing-context, cold-email, marketing-psychology, pricing-strategy, launch-strategy, sales-enablement, skill-creator)
│   ├── SOUL.md                   # universal algorithm, tool discipline, language
│   ├── IDENTITY.md               # delegation table, route actions, zones
│   ├── TOOLS.md                  # subagent list, coordination, retry-limit
│   ├── MEMORY.md                 # corrections log
│   └── skills/                   # all 32 skills (shared across agents via AGENTS.md workaround)
├── workspace-ad-manager/         # ad-manager (6 skills: cabinet, creative-generator, retargeting-funnel, ad-creative, paid-ads, marketing-ideas)
│   ├── SOUL.md                   # retry-limit, known bug warning, action-log
│   ├── IDENTITY.md               # zone of responsibility, routes
│   └── TOOLS.md                  # Meta API retry rules, error table
├── workspace-content-writer/     # content-writer (10 skills: content-creator, seo-optimizer, copywriting, content-strategy, social-content, copy-editing, email-sequence, seo-audit, ai-seo, schema-markup)
│   ├── SOUL.md                   # checklist, zone of responsibility
│   ├── IDENTITY.md               # content pillars, platform formats
│   └── TOOLS.md
├── workspace-competitor-spy/     # competitor-spy (2 skills: ad-spy, competitor-alternatives)
│   ├── SOUL.md                   # zone, retry-limit
│   ├── IDENTITY.md               # routes, other agents table
│   └── TOOLS.md                  # scraper API, DuckDuckGo fallback
├── workspace-analytics-brain/    # analytics-brain (4 skills: ad-analytics, analytics-tracking, ab-test-setup, page-cro)
│   ├── SOUL.md                   # GET only, zone, retry-limit
│   ├── IDENTITY.md               # routes, other agents table
│   └── TOOLS.md                  # Meta insights endpoints
├── shared-skills/                # legacy (5 skills), all skills now in workspace/skills/
└── data/leads.json
```

## Ссылки

- [MiniMax M2.5 Best Practices](https://platform.minimax.io/docs/coding-plan/best-practices)
- [MiniMax M2.5 Announcement](https://www.minimax.io/news/minimax-m25)
- [Anthropic: Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [OpenClaw Configuration Docs](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent)
- [MiniMax M2.5 in Cline](https://cline.bot/blog/minimax-m2-5)
