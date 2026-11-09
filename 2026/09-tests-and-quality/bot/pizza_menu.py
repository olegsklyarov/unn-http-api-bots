import json
from typing import Optional

RECIPES = [
    ("pepperoni", "Пепперони"),
    ("margherita", "Маргарита"),
    ("quatro_formaggi", "Четыре сыра"),
    ("hawaiian", "Гавайская"),
]

SIZES = [
    ("small", "Маленькая"),
    ("medium", "Средняя"),
    ("large", "Большая"),
]

CRUSTS = [
    ("none", "Без бортика"),
    ("regular", "Обычный"),
    ("cheese", "Сырный"),
    ("sausage", "Колбасный"),
]

DRINKS = [
    ("juice", "Сок"),
    ("cola", "Кола"),
    ("tea", "Чай"),
    ("morse", "Морс"),
]

_LABELS = {
    key: label
    for options in (RECIPES, SIZES, CRUSTS, DRINKS)
    for key, label in options
}

MSG_CHOOSE_RECIPE = "Собери пиццу. Выбери рецепт:"
MSG_CHOOSE_SIZE = "Выбери размер:"
MSG_CHOOSE_CRUST = "Выбери бортик:"
MSG_CHOOSE_DRINK = "Выбери напиток:"
MSG_ORDER_FINISHED_HINT = "Заказ уже оформлен. Нажми /start, чтобы начать новый."


def label_for(option_id: str) -> str:
    return _LABELS.get(option_id, option_id)


def _keyboard(prefix: str, options: list[tuple[str, str]]) -> str:
    return json.dumps(
        {
            "inline_keyboard": [
                [{"text": label, "callback_data": f"{prefix}:{key}"}]
                for key, label in options
            ]
        },
        ensure_ascii=False,
    )


def recipes_keyboard() -> str:
    return _keyboard("recipe", RECIPES)


def sizes_keyboard() -> str:
    return _keyboard("size", SIZES)


def crusts_keyboard() -> str:
    return _keyboard("crust", CRUSTS)


def drinks_keyboard() -> str:
    return _keyboard("drink", DRINKS)


def parse_callback_data(data: str, prefix: str) -> Optional[str]:
    expected = f"{prefix}:"
    if not data.startswith(expected):
        return None
    value = data[len(expected) :]
    return value or None


def format_order_summary(order_content: dict) -> str:
    recipe = label_for(order_content["recipe"])
    size = label_for(order_content["size"])
    crust = label_for(order_content["crust"])
    drink = label_for(order_content["drink"])
    return (
        "Заказ принят:\n"
        f"• Рецепт: {recipe}\n"
        f"• Размер: {size}\n"
        f"• Бортик: {crust}\n"
        f"• Напиток: {drink}\n\n"
        "Новый заказ: /start"
    )
