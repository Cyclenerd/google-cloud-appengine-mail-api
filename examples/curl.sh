#!/usr/bin/env bash

# Send email via Mail API
# https://github.com/Cyclenerd/google-cloud-appengine-mail-api

API_PASSWORD='YOUR_API_PASSWORD'

URL='https://PROJECT_ID.REGION_ID.r.appspot.com/messages'

curl -s --user "api:${API_PASSWORD}" \
    $URL \
    -F "to=test@nkn-it.de" \
    -F "subject=curl Example" \
    -F "text=This is a simple test."