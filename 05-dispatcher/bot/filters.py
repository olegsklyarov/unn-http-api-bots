def is_message_with_text(update: dict) -> bool:
    return 'message' in update and 'text' in update['message']

def is_callback_query(update: dict) -> bool:
    return 'callback_query' in update
