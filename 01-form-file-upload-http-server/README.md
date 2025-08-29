Инструкция
==========

```bash
# запустить сервер
python form-file-upload-server.py

# отправить HTTP запрос при помощи утилиты curl
# где /Users/oleg/harry.jpg - заменить на абсолютный путь к файлу для загрузки
curl -X POST -F "file=@/Users/oleg/harry.jpg" http://localhost:8000
```
