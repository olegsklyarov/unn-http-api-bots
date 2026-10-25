import json

from bot import telegram_bot_api, updated_logger, users_storage

INLINE_KEYBOARD = json.dumps(
    {
        "inline_keyboard": [
            [
                {"text": "Сырой JSON", "callback_data": "raw"},
                {"text": "Скрыть", "callback_data": "hide"},
            ]
        ]
    },
    ensure_ascii=False,
)

EMPTY_KEYBOARD = json.dumps({"inline_keyboard": []})


def main():
    next_update_id = 0
    try:
        while True:
            for update in telegram_bot_api.get_updates(
                offset=next_update_id,
                timeout=30,
                # Иначе остаётся прошлый allowed_updates (например только message) —
                # callback_query не приходит, inline-кнопки «не работают».
                allowed_updates=json.dumps(["message", "callback_query"]),
            ):
                next_update_id = max(next_update_id, update["update_id"] + 1)
                updated_logger.persist_update(update)
                users_storage.persist_user(update)
                if "callback_query" in update:
                    cq = update["callback_query"]
                    # Без answerCallbackQuery у кнопки бесконечно крутятся «часики».
                    telegram_bot_api.answer_callback_query(callback_query_id=cq["id"])
                    data = cq.get("data")
                    message = cq.get("message")
                    if message is not None:
                        chat_id = message["chat"]["id"]
                        if data == "raw":
                            reply_to_message = message.get("reply_to_message")
                            if reply_to_message is not None:
                                raw = json.dumps(
                                    reply_to_message,
                                    ensure_ascii=False,
                                    indent=2,
                                )
                                telegram_bot_api.send_message(
                                    chat_id=chat_id,
                                    text=f"```\n{raw}\n```",
                                    parse_mode="Markdown",
                                )
                        elif data == "hide":
                            telegram_bot_api.edit_message_reply_markup(
                                chat_id=chat_id,
                                message_id=message["message_id"],
                                reply_markup=EMPTY_KEYBOARD,
                            )
                    print(".", end="", flush=True)
                    continue
                message = update.get("message")
                if message is None:
                    continue
                chat_id = message["chat"]["id"]
                echo_kwargs = {
                    "chat_id": chat_id,
                    "reply_to_message_id": message["message_id"],
                    "reply_markup": INLINE_KEYBOARD,
                }
                if "text" in message:
                    telegram_bot_api.send_message(**echo_kwargs, text=message["text"])
                elif "sticker" in message:
                    telegram_bot_api.send_sticker(
                        **echo_kwargs,
                        sticker=message["sticker"]["file_id"],
                    )
                elif "video_note" in message:
                    telegram_bot_api.send_video_note(
                        **echo_kwargs,
                        video_note=message["video_note"]["file_id"],
                    )
                else:
                    continue
                print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
