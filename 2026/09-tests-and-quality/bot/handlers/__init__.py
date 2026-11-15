from bot.handler import Handler
from bot.handlers.order_finished import OrderFinished
from bot.handlers.persist_update import PersistUpdate
from bot.handlers.persist_user import PersistUser
from bot.handlers.start_command import StartCommand
from bot.handlers.waiting_for_crust import WaitingForCrust
from bot.handlers.waiting_for_drink import WaitingForDrink
from bot.handlers.waiting_for_pizza_size import WaitingForPizzaSize
from bot.handlers.waiting_for_recipe import WaitingForRecipe


def get_handlers() -> list[Handler]:
    return [
        PersistUpdate(),
        PersistUser(),
        StartCommand(),
        WaitingForRecipe(),
        WaitingForPizzaSize(),
        WaitingForCrust(),
        WaitingForDrink(),
        OrderFinished(),
    ]
