import json

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
    key: label for options in (RECIPES, SIZES, CRUSTS, DRINKS) for key, label in options
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


def parse_callback_data(data: str, prefix: str) -> str | None:
    expected = f"{prefix}:"
    if not data.startswith(expected):
        return None
    value = data[len(expected) :]
    return value or None


_ORDER_FIELDS = (
    ("recipe", "Рецепт"),
    ("size", "Размер"),
    ("crust", "Бортик"),
    ("drink", "Напиток"),
)


def format_order_progress(order_content: dict) -> str:
    lines = []
    for key, title in _ORDER_FIELDS:
        value = order_content.get(key)
        if value is not None:
            lines.append(f"• {title}: {label_for(value)}")
    return "\n".join(lines)


def step_message(order_content: dict, prompt: str) -> str:
    progress = format_order_progress(order_content)
    if not progress:
        return prompt
    return f"Заказ:\n{progress}\n\n{prompt}"


def format_order_summary(order_content: dict) -> str:
    progress = format_order_progress(order_content)
    return f"Заказ принят:\n{progress}\n\nНовый заказ: /start"
