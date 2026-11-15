# Лекция 8. States — pizza shop

Учебный Telegram-бот: заказ пиццы через FSM (finite state machine) поверх паттерна Dispatcher / Handler.

Запуск: `make run` (нужен `.env` с `TELEGRAM_TOKEN`).

## Что делает бот

Диалог на русском, выбор опций — только inline-кнопки (`callback_query`).

1. `/start` — сброс заказа, выбор рецепта
2. размер → бортик → напиток
3. итог заказа; новый заказ снова через `/start`

## FSM

Состояние пользователя хранится в `data/users.json` в поле `state`:

```json
{
  "current_state": "waiting_for_pizza_size",
  "order_content": {
    "recipe": "pepperoni",
    "size": null,
    "crust": null,
    "drink": null
  }
}
```

| `current_state` | Смысл |
|-----------------|--------|
| `waiting_for_recipe` | выбор рецепта (дефолт, если state нет) |
| `waiting_for_pizza_size` | размер |
| `waiting_for_crust` | бортик |
| `waiting_for_drink` | напиток |
| `order_finished` | заказ завершён |

Меню и русские подписи кнопок/текстов — в [`bot/pizza_menu.py`](bot/pizza_menu.py). В `callback_data` и `order_content` — стабильные английские id (`recipe:pepperoni`, …).

`persist_user` **не затирает** `state`: при обновлении профиля Telegram merge сохраняет текущий FSM-снимок; новому пользователю пишется `default_state()`.

## Архитектура

```
__main__ → Dispatcher + handlers → long_polling (getUpdates)
                ↓
         user_id → get_user_state
                ↓
         can_handle(update, state) / handle(update, state)
```

- [`bot/handler.py`](bot/handler.py) — абстрактный `Handler` + `HandlerStatus` (`CONTINUE` / `STOP`)
- [`bot/dispatcher.py`](bot/dispatcher.py) — резолвит state из `files_storage` и передаёт в handlers
- [`bot/storage.py`](bot/storage.py) — интерфейс Storage (`get_user_state` / `save_user_state` / `persist_user` / `persist_update` / `default_state`)
- [`bot/files_storage.py`](bot/files_storage.py) — MVP на JSON-файлах: `users.json` + `data/updates/<update_id>.json`
- [`bot/telegram_bot_api.py`](bot/telegram_bot_api.py) — тонкий HTTP-клиент Bot API (функции)
- [`bot/telegram_messenger.py`](bot/telegram_messenger.py) — реализация `Messenger` поверх `telegram_bot_api`
- [`bot/long_polling.py`](bot/long_polling.py) — цикл `getUpdates` (`message` + `callback_query`)

### Порядок handlers

1. `PersistUpdate`, `PersistUser` — side-effects на диск, `CONTINUE`
2. `StartCommand` — `/start`
3. `WaitingForRecipe` → `WaitingForPizzaSize` → `WaitingForCrust` → `WaitingForDrink`
4. `OrderFinished` — лишний callback после завершения («заказ уже оформлен…»)

Каждый state-handler: проверка `current_state` + префикса `callback_data` → `answerCallbackQuery` → запись в `order_content` → смена стейта → `save_user_state` → следующее сообщение (или summary).

## Каталог `data/`

В `.gitignore` — только локально:

- `data/updates/` — сырые updates для отладки
- `data/users.json` — пользователи + FSM state
