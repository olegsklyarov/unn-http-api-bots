def is_message_with_type(update: dict, message_type: str) -> bool:
    return 'message' in update and message_type in update['message']

def is_callback_query(update: dict) -> bool:
    return 'callback_query' in update
