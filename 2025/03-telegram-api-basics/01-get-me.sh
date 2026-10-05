#!/usr/bin/env bash

source .env

# https://core.telegram.org/bots/api#getme
curl --silent https://api.telegram.org/bot$TELEGRAM_TOKEN/getMe | jq
