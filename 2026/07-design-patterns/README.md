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
| 5 | `2026-fall-07-step-06` | Актуальное состояние пользователей в `data/users.json` |
| 6 | `2026-fall-07-step-07` | Inline-кнопки под echo: сырой JSON и скрыть клавиатуру |
| 7 | `2026-fall-07-step-08` | Telegram Bot API клиент вынесен в `bot/telegram_bot_api.py` |
| 8 | `2026-fall-07-step-09` | Persist updates вынесен в `bot/updated_logger.py` |
| 9 | `2026-fall-07-step-10` | Users storage вынесен в `bot/users_storage.py` |

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

## Шаг 5 — `data/users.json`

На каждый [Update](https://core.telegram.org/bots/api#update) вызываем `persist_user`: из payload по типу update достаём [User](https://core.telegram.org/bots/api#user) (`from` у message/callback_query/… или `user` у poll_answer/business_connection). Если пользователя нет — молча выходим.
Файл `data/users.json` — один JSON-объект: ключ = telegram user id, значение = поля User плюс unix-timestamps `created_at` / `updated_at`. Новый пользователь добавляется; существующий перезаписывается данными из update (они считаются актуальнее), `created_at` сохраняется, `updated_at` всегда обновляется.
Формат: `ensure_ascii=False`, без `indent=2`, ключи отсортированы, одна строка — один пользователь. Пишется для любого update (до веток echo).

## Шаг 6 — inline-кнопки

Под каждым echo (text / sticker / video_note) две [inline-кнопки](https://core.telegram.org/bots/api#inlinekeyboardbutton): «Сырой JSON» и «Скрыть». Echo уходит с `reply_to_message_id`, чтобы в callback было исходное сообщение пользователя.
В `getUpdates` явно передаём `allowed_updates=["message","callback_query"]` — иначе Telegram может оставить прошлый фильтр только на `message`, и клики по кнопкам не доходят.
Сразу после `callback_query` вызываем [`answerCallbackQuery`](https://core.telegram.org/bots/api#answercallbackquery) — иначе у кнопки бесконечно крутятся «часики».
«Сырой JSON»: берём `callback_query.message.reply_to_message` **из update** (не из `data/updates/`) и шлём обычным `sendMessage` **без** `reply_to_message_id`, Markdown code fence (`parse_mode=Markdown`).
«Скрыть»: [`editMessageReplyMarkup`](https://core.telegram.org/bots/api#editmessagereplymarkup) с пустым `inline_keyboard` — клавиатура пропадает.

## Шаг 7 — модуль `bot/telegram_bot_api.py`

HTTP-клиент Telegram Bot API (`api_request`, `get_updates`, `send_message`, …) вынесен из `__main__.py` в отдельный модуль [`bot/telegram_bot_api.py`](bot/telegram_bot_api.py).
В `__main__.py` вызовы через полное имя модуля (`telegram_bot_api.send_message(...)`), чтобы было видно, откуда метод. Транспорт и токен — в одном месте. Первый шаг к разделению ответственности (дальше — design patterns).

## Шаг 8 — модуль `bot/updated_logger.py`

Запись входящих updates на диск (`persist_update` → `data/updates/<update_id>.json`) вынесена в [`bot/updated_logger.py`](bot/updated_logger.py).
В `__main__.py`: `updated_logger.persist_update(update)`. Логика бота и «логгер» updates разделены по модулям.

## Шаг 9 — модуль `bot/users_storage.py`

Работа с `data/users.json` (`persist_user`, `user_from_update`, формат файла) вынесена в [`bot/users_storage.py`](bot/users_storage.py).
В `__main__.py`: `users_storage.persist_user(update)`. Хранение пользователей отделено от цикла обработки updates.

## Переключение шагов

```bash
./demo          # список шагов
./demo next     # следующий
./demo prev     # предыдущий
./demo 1        # к шагу с тегом …-step-01
```
