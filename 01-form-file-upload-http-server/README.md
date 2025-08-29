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
