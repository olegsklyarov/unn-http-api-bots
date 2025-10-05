# Лекция 4. Базовый бот на Python

## Что такое чат-бот в Telegram?

<Архитектурная схема>

1. Особый тип аккаунта. Этот аккаунт управляется программой, а не человеком.
1. Создается через BotFather, не имеет номера телефона (в отличие от обычного ТГ
аккаунта)
1. Логика бота осуществляется программным путем. Для управления используется
стороннее приложение, расположенное на хосте разработчика. Управление по
протоколу HTTP API. Для получения сообщений использует Long polling / Webhook.
1. Ограниченные возможности по сравнению с обычным пользователем.
1. Дает спец возможности:
    1. Inline Mode
    2. Custom Keyboards
    3. Web Apps

### Что хранится в аккаунте бота?
Аккаунт бота похоже на обычного User, но имеет отличия. Хранит состояние:
* Список всех пользователей (чатов), которые запустили бота (может отправлять сообщения только им)
* Буфер / кеш сообщений, которые отправлены боту, но ещё не приняты Web приложением (нашим ботом)
* Настройки клавиатуры (рассмотрим позже)

## Базовый бот на Python

### Выбор хранилища для бота

Задачи:
- Списка пользователей ботов
- Переписка с ботом: журнал входящих и исходящих сообщений
- Состояния общения с каждым пользователем согласно бизнес логики

Варианты: SQL / No SQL, файлы...

SQLite:
- вся БД в одном файле
- не требуется дополнительное ПО, поддержка встроена в Python
- DBeaver

### venv
https://docs.python.org/3/library/venv.html

файл requirements.txt

python -m venv .venv
source ./venv/bin/activate
pip install -r requirements.txt
deactiate 


### Python packages
https://docs.python.org/3/tutorial/modules.html#packages

запуск через $ python -m bot


### Переменные окружения

- python-dotenv - https://pypi.org/project/python-dotenv
- os.getenv() - https://docs.python.org/3/library/os.html#os.getenv

Проектируем сразу для удобного деплоя в облако / интернет, при этом стараемся
излишне не усложнять (читай The Twelve Factors)

Выносим в переменные окружения:
- TELEGRAM_TOKEN
- SQLITE_DATABASE_PATH

### Клиент для работы с БД

Встроенный модуль `sqlite3`
https://docs.python.org/3.13/library/sqlite3.html - д/з пройти туториал

Таблица для хранения входящих сообщений telegram_updates

### Клиент для запросов в Telegram Bot API

Модули:
- urllib.request - https://docs.python.org/3/library/urllib.request.html
- json - https://docs.python.org/3/library/json.html

### Собираем main цикл
- контролируем getUpdates, offset
- логика echo бота (то что делали дома руками)
- корректная остановка по Ctrl+C
