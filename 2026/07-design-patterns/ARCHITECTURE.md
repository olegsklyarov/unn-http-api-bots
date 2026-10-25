# Архитектура: Dispatcher / Handler

Диаграммы к шагу 10 (тег `2026-fall-07-step-11`). Паттерн — [цепочка обязанностей](https://refactoring.guru/ru/design-patterns/chain-of-responsibility); контракт handlers — [`abc`](https://docs.python.org/3/library/abc.html).

## Как это работает во времени (для доски)

```mermaid
sequenceDiagram
  participant Main
  participant LP as long_polling
  participant API as telegram_bot_api
  participant D as Dispatcher
  participant P as PersistUpdate
  participant U as PersistUser
  participant H as EchoOrCallback

  Main->>D: add_handlers(...)
  Main->>LP: start_long_polling(D)
  loop каждый цикл
    LP->>API: getUpdates
    API-->>LP: updates
    loop каждый update
      LP->>D: dispatch(update)
      D->>P: can_handle? True
      D->>P: handle → CONTINUE
      D->>U: can_handle? True
      D->>U: handle → CONTINUE
      D->>H: can_handle?
      alt подходит
        D->>H: handle → STOP
        Note over D: break — дальше не идём
      else не подходит
        D->>H: пропуск
      end
    end
  end
```

Persist-handlers всегда срабатывают и возвращают `CONTINUE`. Узкий echo/callback при совпадении возвращает `STOP` — цепочка обрывается.

## UML-подобная диаграмма структуры

```mermaid
classDiagram
  direction TB

  class HandlerStatus {
    <<enumeration>>
    CONTINUE
    STOP
  }

  class Handler {
    <<abstract>>
    +can_handle(update) bool
    +handle(update) HandlerStatus
  }

  class Dispatcher {
    -handlers: list~Handler~
    +add_handlers(*handlers)
    +dispatch(update)
  }

  class PersistUpdate
  class PersistUser
  class CallbackRawJson
  class CallbackHide
  class MessageEchoText
  class MessageEchoSticker
  class MessageEchoVideoNote

  Handler --> HandlerStatus : returns
  Dispatcher o--> Handler : содержит*
  Handler <|-- PersistUpdate
  Handler <|-- PersistUser
  Handler <|-- CallbackRawJson
  Handler <|-- CallbackHide
  Handler <|-- MessageEchoText
  Handler <|-- MessageEchoSticker
  Handler <|-- MessageEchoVideoNote

  PersistUpdate ..> updated_logger : persist_update
  PersistUser ..> users_storage : persist_user
  CallbackRawJson ..> telegram_bot_api
  CallbackHide ..> telegram_bot_api
  MessageEchoText ..> telegram_bot_api
  MessageEchoSticker ..> telegram_bot_api
  MessageEchoVideoNote ..> telegram_bot_api
```

## Упрощённый вид «только паттерн» для слайда

```mermaid
classDiagram
  class Client {
    long_polling / main
  }
  class Dispatcher {
    dispatch(request)
  }
  class Handler {
    <<abstract>>
    can_handle(request)
    handle(request)
  }
  class ConcreteHandlerA
  class ConcreteHandlerB

  Client --> Dispatcher : передаёт update
  Dispatcher --> Handler : по очереди
  Handler <|-- ConcreteHandlerA
  Handler <|-- ConcreteHandlerB
```
