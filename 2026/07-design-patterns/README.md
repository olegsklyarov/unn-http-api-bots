# Лекция 7. Design patterns

Демо шаги переключаются через `./demo` (теги `2026-fall-07-step-NN`).
Запуск бота: `make run` (нужен `.env` с `TELEGRAM_TOKEN`).

| Шаг | Тег | Описание |
|-----|-----|----------|
| 0 | `2026-fall-07-step-01` | Базовый echo-бот с предыдущей лекции |
| 1 | `2026-fall-07-step-02` | История всех входящих updates на диске — изучать структуру, обучение и дебаг |
| 2 | `2026-fall-07-step-03` | Ответ только на text; остальное игнорируем без падения |
| 3 | `2026-fall-07-step-04` | Echo стикера через новый метод API `sendSticker` |
| 4 | `2026-fall-07-step-05` | Echo кружка (video note) через `sendVideoNote` |

## Шаг 0 — echo-бот

Тот же бот, что на прошлой лекции: long polling через `getUpdates`, ответ тем же текстом через `sendMessage`.

## Шаг 1 — persist updates

Каждый входящий update сохраняется в `data/updates/<update_id>.json` (`ensure_ascii=False`, `indent=2`).
Каталог `data/` в `.gitignore` — файлы только локально, для разбора структуры Update и отладки.

## Шаг 2 — только text

У `Message` не всегда есть `text` (стикер, фото, …), а у Update — не всегда `message`. Без проверки бот падает на `KeyError`.
Теперь: `data/updates` пишется для любого update; `sendMessage` — только если есть `message` с полем `text`. Остальное молча пропускаем.

## Шаг 3 — echo стикеров

У входящего `Message` может быть поле `sticker` (см. JSON в `data/updates`) с `file_id`.
Добавляем ещё один метод Telegram Bot API — [`sendSticker`](https://core.telegram.org/bots/api#sendsticker) (хелпер `send_sticker` рядом с уже существующим `sendMessage`).
В параметр `sticker` передаём тот же `file_id` из входящего сообщения — файл качать не нужно.
Text по-прежнему echo через `sendMessage`; всё остальное игнорируем без падения; `data/updates` пишется всегда.

## Шаг 4 — echo video note

У входящего `Message` может быть поле `video_note` (см. JSON в `data/updates`) с `file_id`.
Добавляем ещё один метод Telegram Bot API — [`sendVideoNote`](https://core.telegram.org/bots/api#sendvideonote) (хелпер `send_video_note`).
В параметр `video_note` передаём тот же `file_id` из входящего сообщения — файл качать не нужно.
Text и sticker по-прежнему echo; всё остальное игнорируем без падения; `data/updates` пишется всегда.

## Переключение шагов

```bash
./demo          # список шагов
./demo next     # следующий
./demo prev     # предыдущий
./demo 1        # к шагу с тегом …-step-01
```
