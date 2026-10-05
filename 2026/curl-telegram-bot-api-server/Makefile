include .env

.PHONY: getMe getUpdates getUpdatesJson getUpdatesUrlencode sendMessage

getMe:
	curl --silent https://api.telegram.org/bot$(TELEGRAM_TOKEN)/getMe | jq

getUpdates:
	curl \
		--silent \
		-X POST \
		-H "Content-Type: application/json" \
		-d '{ \
			"offset": 592752087, \
			"timeout": 30, \
			"allowed_updates": ["message"] \
		}' \
		https://api.telegram.org/bot$(TELEGRAM_TOKEN)/getUpdates | jq

getUpdatesJson:
	curl \
		--silent \
		-X POST \
		-H "Content-Type: application/json" \
		-d @get-updates-request.json \
		https://api.telegram.org/bot$(TELEGRAM_TOKEN)/getUpdates | jq

getUpdatesUrlencode:
	curl \
		--silent \
		-G \
		--data-urlencode 'offset=592752087' \
		--data-urlencode 'timeout=30' \
		--data-urlencode 'allowed_updates=["message"]' \
		https://api.telegram.org/bot$(TELEGRAM_TOKEN)/getUpdates | jq

sendMessage:
	curl \
		--silent \
		-X POST \
		-H "Content-Type: application/json" \
		-d @send-message-request.json \
		https://api.telegram.org/bot$(TELEGRAM_TOKEN)/sendMessage | jq
