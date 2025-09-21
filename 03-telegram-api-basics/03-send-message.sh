#!/usr/bin/env bash

source .env

# https://core.telegram.org/bots/api#sendmessage
curl \
    --silent \
    -X POST \
    -H "Content-Type: application/json" \
    -d @03-send-message-request.json \
    https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage | jq
