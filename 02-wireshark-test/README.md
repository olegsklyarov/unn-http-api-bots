## Замечания про HTTP

- Сетевая модель OSI: стек протоколов, инкапсуляция aka "матрешка" или "стек почтовых конвертов"
- Первоисточник - стандарты RFC, публикуются организацией https://www.ietf.org. Сайт https://www.rfc-editor.org. Примеры:
  - [RFC 793 Transmission Control Protocol, September 1981](https://www.rfc-editor.org/info/rfc793)
  - [RFC 791 Internet Protocol, September 1981](https://www.rfc-editor.org/info/rfc791)

## Принципы шифрования данных (подходим к HTTPS)

message - сообщение
Alice: PrivateKey_Alice, PublicKey_Alice
Bob: PrivateKey_Bob, PublicKey_Bob

Элис хочет отправить сообщение message Бобу, чтобы никто кроме Боба не мог его прочитать.

1. Элис запрашивает у Боба его PublicKey_Bob
2. Элис шифрует свое сообщение message_encrypted = Encrypt(message, PublicKey_Bob)
3. Элис отправляет message_encrypted Бобу по незащищенному каналу.
4. Боб расшифровывает message_decrypted = Decrypt(message_encrypted, PrivateKey_Bob)

На выходе имеем: message == message_decrypted.

То есть message == Decrypt(Encrypt(message, PublicKey_Bob), PrivateKey_Bob)

Правила безопасности:
- Открытый ключ можно и нужно опубликовать в открытом доступе для всех желающих. Например см. https://keys.openpgp.org
- Приватный ключ храним в секрете!!!


## Практика шифрования файла при помощи GNU Privacy Guard (GPG)

https://gnupg.org

Задача: Элис требуется отправить файл message.txt Бобу так, чтобы никто кроме Боба не мог прочитать этот файл.

```bash
# Боб создает связку GPG ключей: name = Bob, email = bob@example.com
(Bob) $ gpg --full-gen-key

# Боб делает экспорт открытого ключа, чтобы передать его Элис
(Bob) $ gpg --export -a bob@example.com > bob_public.gpg

# Боб отправляет файл bob_public.gpg Элис доступным способом (почта, telegram, флешка и тп)

# Элис импортирует ключ Боба в GPG
(Alice) $ gpg --import bob_public.gpg

# Элис делает ключ Боба доверенным
(Alice) $ gpg --edit-key bob@example.com
> trust
> 5
> quit

# Элис шифрует файл с сообщением при помощи открытого ключа Боба
(Alice) $ gpg -e -a -r bob@example.com message.txt

# Элис отправляет зашифрованный файл message.txt.asc Бобу

# Боб расшифровывает message.txt.asc
(Bob) $ gpg -d -o message.txt message.txt.asc
```

### Полезные команды

```bash
# список открытых ключей
$ gpg -k

# список секретных ключей
$ gpg -K
```

## Смотрим HTTP трафик

```bash
# установка wireshark
$ sudo apt install wireshark
$ sudo dpkg-reconfigure wireshark-common
$ sudo chmod +x /usr/bin/dumpcap

# запускаем wireshark
$ wireshark

# запускаем HTTP сервер
$ python3 http-server.py

# отправляем HTTP запрос
$ curl "http://127.0.0.1:8000?login=user&password=passwd"
```

## Смотрим HTTPS трафик

```bash
# Генерируем самоподписанный ключ и сертификат
$ openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem

# запускаем HTTPS сервер
$ python3 https-server.py

# отправляем HTTPS запрос
$ curl https://127.0.0.1:8443

# отправляем HTTPS запрос (разрешаем самоподписанный сертификат)
$ curl --insecure "https://127.0.0.1:8443?login=user&password=passwd"
```

В каждом запросе в телеграмм используется секретный access token прямо. Это можно делать только в HTTPS!

## Ссылки
https://www.cloudflare.com/learning/ssl/why-is-http-not-secure/


## JSON

JavaScript Object Notation
- human-readable
- https://docs.python.org/3/library/json.html
- https://jsonpath.com


# Введение в телеграм боты

https://core.telegram.org/mtproto

HTTP Bot API vs MTProto
![HTTP Bot API vs MTProto](mtproto-vs-bot-api.png)

https://docs.telethon.dev/en/stable/concepts/botapi-vs-mtproto.html
https://docs.pyrogram.org/faq/why-is-the-api-key-needed-for-bots


https://core.telegram.org/bots
https://core.telegram.org/bots/api

1. Бот - это особый вид пользователя Telegram.
2. Создается только через BotFather.
3. Не может написать первым (уважает приватность пользователей, так Bot API избегает спама)
4. За логику бота отвечает пользовательская программа, которая общается с Bot API по HTTPS протоколу.


Authorizing your bot

Making requests

Getting updates: long pooling / webhooks

Чтобы бот отправил бот сообщение пользователю - просто вызываем метод sendMessage

Отправляем сообщение

Получаем сообщения при помощи getUpdates. Исследуем как отметить сообщение прочитанным!

Работаем сначала на голых curl запросах.

Заготовка бота https://github.com/dinara-urazova/arithmetic_bot/blob/main/bot/__main__.py