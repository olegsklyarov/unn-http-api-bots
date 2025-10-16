from bot.handler import Handler
from bot.handlers.callback_cancel import CallbackCancel
from bot.handlers.message_button_inline import MessageButtonInline
from bot.handlers.message_document import MessageDocument
from bot.handlers.message_voice import MessageVoice
from bot.handlers.message_audio import MessageAudio
from bot.handlers.message_animation import MessageAnimation
from bot.handlers.message_video import MessageVideo
from bot.handlers.message_video_note import MessageVideoNote
from bot.handlers.message_sticker import MessageSticker
from bot.handlers.message_contact import MessageContact
from bot.handlers.message_location import MessageLocation
from bot.handlers.message_venue import MessageVenue
from bot.handlers.message_poll import MessagePoll
from bot.handlers.message_dice import MessageDice
from bot.handlers.message_photo import MessagePhoto
from bot.handlers.message_start import MessageStart
from bot.handlers.update_database_logger import UpdateDatabaseLogger


def get_handlers() -> list[Handler]:
    return [
        UpdateDatabaseLogger(),
        MessageStart(),
        MessageButtonInline(),
        CallbackCancel(),
        MessageDocument(),
        MessageVoice(),
        MessageAudio(),
        MessageAnimation(),
        MessageVideo(),
        MessageVideoNote(),
        MessageSticker(),
        MessageContact(),
        MessageLocation(),
        MessageVenue(),
        MessagePoll(),
        MessageDice(),
        MessagePhoto(),
    ]
