# Лекция 2. Защищенная передача данных. Просмотр трафика. JSON.

## Защищенная передача данных

### Дано
- Alice — отправитель сообщения `message`
- Bob — получатель (`PrivateKey_Bob`, `PublicKey_Bob`)

### Задача
Элис требуется отправить сообщение message Бобу, чтобы никто кроме Боба не мог его прочитать.

### Алгоритм

1. Элис запрашивает у Боба его `PublicKey_Bob`
1. Элис шифрует свое сообщение `message_encrypted = Encrypt(message, PublicKey_Bob)`
1. Элис отправляет `message_encrypted` Бобу по незащищенному каналу.
1. Боб расшифровывает `message_decrypted = Decrypt(message_encrypted, PrivateKey_Bob)`

На выходе имеем: `message == message_decrypted`.

То есть `message == Decrypt(Encrypt(message, PublicKey_Bob), PrivateKey_Bob)`

### Правила безопасности
- Открытый ключ можно и нужно опубликовать в открытом доступе для всех желающих. Например см. https://keys.openpgp.org
- Приватный ключ храним в секрете!!!


## Практика шифрования файла при помощи GNU Privacy Guard (GPG)

https://gnupg.org

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

## Просмотр сетевого трафика

### Замечания про HTTP

- Сетевая модель OSI: стек протоколов, инкапсуляция ("матрешка")
- Первоисточник: стандарты RFC, публикуются организацией https://www.ietf.org. Сайт https://www.rfc-editor.org. Примеры:
  - [RFC 793 Transmission Control Protocol, September 1981](https://www.rfc-editor.org/info/rfc793)
  - [RFC 791 Internet Protocol, September 1981](https://www.rfc-editor.org/info/rfc791)

### Смотрим HTTP трафик

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

https://www.cloudflare.com/learning/ssl/why-is-http-not-secure/

### Смотрим HTTPS трафик

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

В каждом запросе в телеграмм используется секретный access token. Это можно делать только в HTTPS!


## JSON

JavaScript Object Notation
- human-readable
- https://docs.python.org/3/library/json.html
- https://jsonpath.com
