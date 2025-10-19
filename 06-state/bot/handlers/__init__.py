from bot.handlers.handler import Handler
from bot.handlers.ensure_user_exists import EnsureUserExists
from bot.handlers.message_start import MessageStart
from bot.handlers.order_approval import OrderApprovalHandler
from bot.handlers.pizza_drinks import PizzaDrinksHandler
from bot.handlers.pizza_selection import PizzaSelectionHandler
from bot.handlers.pizza_size import PizzaSizeHandler
from bot.handlers.update_database_logger import UpdateDatabaseLogger


def get_handlers() -> list[Handler]:
    return [
        UpdateDatabaseLogger(),
        EnsureUserExists(),
        MessageStart(),
        PizzaSelectionHandler(),
        PizzaSizeHandler(),
        PizzaDrinksHandler(),
        OrderApprovalHandler(),
    ]
