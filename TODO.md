# TODO — Sumbawa OpenClaw

## Критичное

- [ ] Заменить properties.md на реальные данные (GPS, цены, площади, фото) — сейчас placeholder
- [ ] Купить домен sumbawa.estate
- [ ] Подключить WhatsApp канал для клиентов (создать, отсканировать QR, настроить pairing)
- [ ] Активировать follow-up скилл (сейчас DORMANT — ждёт WhatsApp)

## Контент & Автопостинг

- [ ] Создать Facebook Page для Sumbawa Estate (нужна для Meta Graph API)
- [ ] Подключить Instagram Business аккаунт к FB Page → получить Graph API токен
- [ ] Настроить автопостинг Instagram через Meta Graph API в openclaw
- [ ] Пополнить Anthropic API → протестировать content-writer агента (Claude Sonnet)
- [ ] Сделать drone видео/фото участков — главный формат для продаж
- [ ] Добавить раздел /blog/ на сайт
- [ ] Рассмотреть TikTok (пустой рынок в нише)

## Выполнено (2026-03-03)

- [x] Починить Telegram stuck — отключён health-monitor (`channelHealthCheckMinutes: 0`), false positive каждые 35 мин из-за hardcoded staleEventThreshold 30 мин
- [x] Домен: sumbawa.land → sumbawa.estate во всех файлах (6 файлов)
- [x] FAQ: PT PMA capital обновлён (IDR 10B → 2.5B, BKPM Reg 5/2025), аэропорт Kiantar
- [x] Brand voice — проверен, ок
- [x] Anthropic провайдер настроен: claude-sonnet-4-6, агент content-writer (только content-creator + seo-optimizer)
- [x] Вычищены ВСЕ упоминания East Sumbawa (Lakey Peak, Hu'u, Dompu, Sape, Tambora, Bima) из всех файлов
- [x] properties.md: убраны 4 восточных участка, осталось 2 (Kertasari, Poto Tano)
- [x] Сайт: удалены 4 property cards, 4 gallery items, 4 map markers, карта переценрирована на West Sumbawa
- [x] Content strategy, SEO keywords, hashtags — переписаны на West Sumbawa surf spots
- [x] Сайт проверен — собран в /root/sumbawa-land/, не задеплоен

## Настройка

- [ ] Задеплоить сайт на sumbawa.estate когда домен будет готов
- [ ] Обновить контакты на сайте (WhatsApp, Telegram, email — сейчас placeholder)
- [ ] Добавить свой Brave Search API key (сейчас используется ключ из контейнера)

## Позже

- [ ] Русскоязычный контент — вторая по важности аудитория
- [ ] shared-context/THESIS.md — текущая стратегия/видение проекта
- [ ] HEARTBEAT.md — добавить реальные чеки когда будет WhatsApp + лиды
- [ ] Второй агент (research/intel) — по модели из поста Shubham'а
- [ ] Paid Ads — когда будет Instagram + контент, подключить скиллы meta-ads из ClawHub
