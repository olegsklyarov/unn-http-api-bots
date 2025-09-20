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

## Ссылки
https://www.cloudflare.com/learning/ssl/why-is-http-not-secure/