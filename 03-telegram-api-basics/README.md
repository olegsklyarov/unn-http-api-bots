# Лекция 3. Введение в Telegram Bot API.

## Инструменты взаимодействия с Telegram

### Протокол MTProto

- [MTProto](https://core.telegram.org/mtproto) — протокол передачи данных в Telegram

### MTProto библиотеки
- [TDLib (Telegram Database Library)](https://core.telegram.org/tdlib) — Cross-platform library for building Telegram clients ([GitHub](https://github.com/tdlib/td))
- [Telethon](https://docs.telethon.dev) — Pure Python 3 MTProto API Telegram client library, for bots too!
- [Pyrogram](https://docs.pyrogram.org) — Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots

### Telegram Bots
- [Bots API](https://core.telegram.org/bots) — сервис, предоставляющий HTTP API интерфейс к Telegram
- Сравнение [Bot API vs. MTProto](https://docs.telethon.dev/en/stable/concepts/botapi-vs-mtproto.html)

HTTP Bot API vs MTProto
![HTTP Bot API vs MTProto](mtproto-vs-bot-api.png)

## Основная документация

- [Bots: An introduction for developers](https://core.telegram.org/bots)
- ❗[Telegram Bot API](https://core.telegram.org/bots/api) — главная документация по Bot API

## Коротко про боты
1. Бот — это особый вид пользователя Telegram, имеет меньше привилегий.
1. Создается только через https://t.me/BotFather
1. За логику бота отвечает пользовательская программа, которая общается с Bot API по HTTPS протоколу.
1. Не может написать первым (уважает приватность пользователей, так Bot API избегает спама)

## Практика

### Используемые инструменты

- [curl](https://curl.se)
- [jq](https://jqlang.org)

### Авторизация бота, метод getMe

См. [getMe](./01-get-me.sh)

### Получение обновлений, метод getUpdates

- Long pooling vs. Webhooks
- Как отметить сообщение прочитанным (offset)

См. [getUpdates](./02-get-updates.sh)

### Отправка сообщений, метод sendMessage

- Бот не может первым написать сообщение пользователю. Сначала обычный пользователь должен запустить бот `/start`.

См. [sendMessage](./03-send-message.sh)

### Простейший бот на Python

```bash
# установка https://docs.python.org/3/library/venv.html
$ sudo apt update
$ sudo apt install libpython3-dev python3-venv
```

См. [basic-bot](./04-basic-bot)
