def is_message_with_text(update: dict) -> bool:
    return 'message' in update and 'text' in update['message']

def is_callback_query(update: dict) -> bool:
    return 'callback_query' in update

def is_message_with_photo(update: dict) -> bool:
    return 'message' in update and 'photo' in update['message']

def is_message_with_document(update: dict) -> bool:
    return 'message' in update and 'document' in update['message']

def is_message_with_voice(update: dict) -> bool:
    return 'message' in update and 'voice' in update['message']

def is_message_with_audio(update: dict) -> bool:
    return 'message' in update and 'audio' in update['message']

def is_message_with_animation(update: dict) -> bool:
    return 'message' in update and 'animation' in update['message']

def is_message_with_video(update: dict) -> bool:
    return 'message' in update and 'video' in update['message']

def is_message_with_video_note(update: dict) -> bool:
    return 'message' in update and 'video_note' in update['message']

def is_message_with_sticker(update: dict) -> bool:
    return 'message' in update and 'sticker' in update['message']

def is_message_with_contact(update: dict) -> bool:
    return 'message' in update and 'contact' in update['message']

def is_message_with_location(update: dict) -> bool:
    return 'message' in update and 'location' in update['message']

def is_message_with_venue(update: dict) -> bool:
    return 'message' in update and 'venue' in update['message']

def is_message_with_poll(update: dict) -> bool:
    return 'message' in update and 'poll' in update['message']

def is_message_with_dice(update: dict) -> bool:
    return 'message' in update and 'dice' in update['message']
