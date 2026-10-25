import json  # разбор JSON-ответа Telegram (bytes → dict)
import os  # чтение переменных окружения (BASE_URL, TELEGRAM_TOKEN)
import urllib.parse  # кодирование параметров запроса в form-urlencoded
import urllib.request  # HTTP-клиент: отправка запросов к Telegram Bot API

# Обязательные настройки из окружения (без них бот не запустится)
BASE_URL = os.environ["BASE_URL"]  # адрес Telegram Bot API (например, https://api.telegram.org)
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]  # токен бота от @BotFather


def request_telegram_bot_api(method, **params):
    """HTTP POST запрос к методу Telegram Bot API с возвратом поля result."""
    url = f"{BASE_URL}/bot{TELEGRAM_TOKEN}/{method}"
    # https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
    request = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(params).encode(),
        method="POST",
    )
    with urllib.request.urlopen(request) as r:
        payload = json.loads(r.read())
    # Telegram всегда отвечает JSON с полем ok; при ошибке — description
    if not payload["ok"]:
        raise RuntimeError(payload["description"])
    return payload["result"]


# offset — идентификатор следующего обновления, чтобы не получать уже обработанные
# изначально устанавливаем в 0, чтобы получить все обновления
offset = 0

# Бесконечный цикл: снова и снова запрашиваем обновления у Telegram
while True:
    updates = request_telegram_bot_api(
        # https://core.telegram.org/bots/api#getupdates
        "getUpdates",
        # пометить прошлые сообщения как прочитанные (подтверждённые)
        offset=offset,
        # включить long polling: сервер ждёт до 30 с, пока появятся обновления
        timeout=30,
        # фильтр: API отдаёт только message (остальные типы игнорируются)
        # для form-urlencoded массив передаём как JSON-строку
        allowed_updates=json.dumps(["message"]),
    )

    # Один ответ getUpdates — это список (пачка) событий, а не одно сообщение.
    for update in updates:
        # offset = highest(update_id) + 1 (см. параметр offset в getUpdates)
        offset = max(offset, update["update_id"] + 1)        
        message = update["message"]
        if "text" not in message:
            # message без text (стикер, фото, …) — пропускаем
            continue
        request_telegram_bot_api(
            # https://core.telegram.org/bots/api#sendmessage
            "sendMessage",
            # эхо: отправляем обратно тот же чат
            chat_id=message["chat"]["id"],
            # и тот же текст
            text=message["text"],
        )
        print(".")  # индикатор, что одно событие из пачки обработано

