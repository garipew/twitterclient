#!/usr/bin/env bash

source .env

bearer_response=$(curl -u "$API_KEY:$API_SECRET_KEY" \
	--data 'grant_type=client_credentials' \
	'https://api.x.com/oauth2/token')

BEARER_TOKEN=$(jq '.access_token' <(echo $bearer_response))
echo BEARER_TOKEN="$BEARER_TOKEN" >> .env
