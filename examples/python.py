# Send email via Mail API
# https://github.com/Cyclenerd/google-cloud-appengine-mail-api

import requests

api_password = "YOUR_API_PASSWORD"

url = "https://PROJECT_ID.REGION_ID.r.appspot.com/messages"

payload = {
    'to': 'test@nkn-it.de',
    'subject': 'Python Example',
    'text': 'This is a simple test.'
}

response = requests.request("POST", url, data=payload, auth=('api', api_password))

print(response.text)
