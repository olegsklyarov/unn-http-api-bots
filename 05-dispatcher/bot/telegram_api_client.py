import json
import os
import urllib.request

from dotenv import load_dotenv

load_dotenv()


def make_request(method: str, **kwargs) -> dict:
    json_data = json.dumps(kwargs).encode('utf-8')

    request = urllib.request.Request(
        method='POST',
        url=f"{os.getenv("TELEGRAM_BASE_URI")}/{method}",
        data=json_data,
        headers={
            'Content-Type': 'application/json',
        },
    )

    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')
        response_json = json.loads(response_body)
        assert response_json["ok"] == True
        return response_json["result"]


def get_updates(**kwargs) -> dict:
    """
    https://core.telegram.org/bots/api#getupdates
    """
    return make_request("getUpdates", **kwargs)


def send_message(chat_id: int, text: str, **kwargs) -> dict:
    """
    https://core.telegram.org/bots/api#sendmessage
    """
    return make_request("sendMessage", chat_id=chat_id, text=text, **kwargs)


def answer_callback_query(callback_query_id: str, **kwargs) -> dict:
    """
    https://core.telegram.org/bots/api#answercallbackquery
    """
    return make_request("answerCallbackQuery", callback_query_id=callback_query_id, **kwargs)


def delete_message(chat_id: int, message_id: int) -> dict:
    """
    https://core.telegram.org/bots/api#deletemessage
    """
    return make_request("deleteMessage", chat_id=chat_id, message_id=message_id)
