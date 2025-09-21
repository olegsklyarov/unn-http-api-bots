#!/usr/bin/env bash

source .env

# https://core.telegram.org/bots/api#getupdates
curl \
    --silent \
    -X POST \
    -H "Content-Type: application/json" \
    -d @02-get-updates-request.json \
    https://api.telegram.org/bot$TELEGRAM_TOKEN/getUpdates | jq
