from bot.handler import Handler
from bot.handlers.callback_hide import CallbackHide
from bot.handlers.callback_raw_json import CallbackRawJson
from bot.handlers.message_echo_sticker import MessageEchoSticker
from bot.handlers.message_echo_text import MessageEchoText
from bot.handlers.message_echo_video_note import MessageEchoVideoNote
from bot.handlers.persist_update import PersistUpdate
from bot.handlers.persist_user import PersistUser


def get_handlers() -> list[Handler]:
    return [
        PersistUpdate(),
        PersistUser(),
        CallbackRawJson(),
        CallbackHide(),
        MessageEchoText(),
        MessageEchoSticker(),
        MessageEchoVideoNote(),
    ]
