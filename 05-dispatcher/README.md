# Лекция 5. Диспетчер

## Клавиатуры в чат-ботах

### 🔎 Фильтр апдейтов в Telegram Bot API

Настраивается параметром `allowed_updates` у метода [getUpdates](https://core.telegram.org/bots/api#getupdates). Должен
быть разрешен `callback_query`!

❗Если до Вас ботом владел кто-то другой, то обязательно настраиваем этот параметр.

### ⌨️ Как добавить клавиатуру?

Настраивается параметром `reply_markup` у метода [sendMessage](https://core.telegram.org/bots/api#sendmessage).

* Клавиатура под блоком ввода сообщения [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup)
    * При нажатии — просто вставляет в чат текст, написанный на кнопке. В бот приходит обычный update с `message` и
      `text`.
    * Убрать клавиатуру — [ReplyKeyboardRemove](https://core.telegram.org/bots/api#replykeyboardremove). ❗Если до Вас
      ботом владел кто-то другой, то обязательно вызываем этот метод для сброса клавиатуры.
* Клавиатура под сообщением в области
  чата [InlineKeyboardMarkup](https://core.telegram.org/bots/api#inlinekeyboardmarkup)
    * При нажатии (если у inline кнопки указан параметр `callback_data`) — в бот приходит update с типом
      `callback_query`, а `message` отсутствует!
    * См. [CallbackQuery](https://core.telegram.org/bots/api#callbackquery) для правильной обработки этого апдейта.
      Главное — обязательно вызвать метод
      [answerCallbackQuery](https://core.telegram.org/bots/api#answercallbackquery).

Удалить сообщения из чата — [deleteMessage](https://core.telegram.org/bots/api#deletemessage). Например может быть
полезно для inline кнопки «Отмена».


### 🍝 Spaghetti code 
_(макаронный код, индусский код)_

При прямолинейном подходе, обработчик результатов вызова [getUpdates](https://core.telegram.org/bots/api#getupdates)
превращается в «spaghetti code» — много вложенных `if`-ов, которые тяжело поддерживать. Значительно возрастает
вероятность багов 🐞.

## Паттерн Observer
_(aka. Event-Subscriber, Listener)_

https://refactoring.guru/design-patterns/observer

## Реализуем диспетчер и обработчики

TODO

## Пример приложения

TODO
