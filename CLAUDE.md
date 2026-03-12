# Sumbawa OpenClaw — Документация проекта

## Рабочий цикл (ЧИТАЙ ПЕРВЫМ)

Код редактируется **локально**, а всё серверное (Docker, агенты, скрипты) запускается через SSH.

**SSH alias:** `alla` = `root@178.16.140.84`
**Серверный путь:** `/root/sumbawa-openclaw`

### Как вносить изменения

```bash
# 1. Отредактировал файлы локально
# 2. Закоммитил и запушил
git add -A && git commit -m "описание" && git push

# 3. Подтянул на сервере
ssh alla "cd /root/sumbawa-openclaw && git pull"

# 4. Если менял скилы/конфиг — рестарт контейнера
ssh alla "docker restart sumbawa-agent"
```

### Серверные команды (всегда через ssh alla)

```bash
# Здоровье агентов
ssh alla "docker exec sumbawa-agent openclaw health"

# Тест агента (Petu)
ssh alla "docker exec sumbawa-agent openclaw agent --agent sumbawa --message 'текст' --timeout 120 --json"

# Логи
ssh alla "docker logs sumbawa-agent --tail 50"

# Статус контейнеров
ssh alla "docker ps --filter name=sumbawa"
```

### При изменении скилов (полный цикл)

1. Отредактировать файлы скила локально
2. `git push` → `ssh alla "cd /root/sumbawa-openclaw && git pull"`
3. Почистить сессии: `ssh alla "docker exec sumbawa-agent sh -c 'rm -f /root/.openclaw/agents/sumbawa/sessions/sessions.json /root/.openclaw/agents/sumbawa/sessions/*.jsonl'"`
4. Рестарт: `ssh alla "docker restart sumbawa-agent"`

### Данные (только на сервере, НЕ в git)

- `data/leads.json` — лиды
- `.env` — ключи API (MiniMax, Meta Ads, Google Ads, Telegram)

---

## Что это

Продажа земли в West Sumbawa (Индонезия). 5 AI-агентов на MiniMax в Docker + скрапер.

- **Владелец:** ac1b (@detroitty, Telegram ID 802940343)
- **Бот:** @sumbawa1_bot
- **Контейнеры:** `sumbawa-agent` + `sumbawa-scraper`
- **Статический сайт:** `/root/sumbawa-land/` → http://178.16.140.84/sumbawa/
- **География:** ONLY West Sumbawa. Never mention East Sumbawa.

## Агенты (5, все MiniMax M2.5)

```
PETU (sumbawa) — диспетчер + продажи (10 скилов)
├── content-writer    — контент (10 скилов)
├── competitor-spy    — разведка конкурентов (2 скила)
├── ad-manager        — реклама Meta/Google (6 скилов)
└── analytics-brain   — аналитика (4 скила)
```

## Участки

1. Beachfront, Kertasari — 2,500 m², $45K
2. Coastal, Poto Tano — 10,000 m², $95K

## Подробности архитектуры → `ARCHITECTURE.md`
