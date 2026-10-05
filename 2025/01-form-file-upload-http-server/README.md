Инструкция
==========

```bash
# ИЛИ запустить сервер на Python
python form-file-upload-server.py

# ИЛИ запустить сервер на PHP
php -S 0.0.0.0:8000 form-file-upload-server.php

# отправить HTTP запрос при помощи утилиты curl
# где /Users/oleg/harry.jpg - заменить на абсолютный путь к файлу для загрузки
curl -X POST -F "file=@/Users/oleg/harry.jpg" http://localhost:8000
```

Демо с помощью ngrok / xtunnel.ru
=================================

1. Установить ngrok / xtunnel.ru
2. Запустить HTTP сервер по инструкции выше
3. Опубликовать в Интернет ngrok / xtunnel.ru
4. Создать QR код для сканирования http://qrcoder.ru

Лимиты на загрузку в PHP
========================
Настроить лимит на размер загружаемого файла можно в php.ini

```
upload_max_filesize=10M
post_max_size=10M
```

Полезные ссылки
===============

Ищем альтернативу Ngrok в России
https://habr.com/ru/articles/833884/
