# Send email via Mail API
# https://github.com/Cyclenerd/google-cloud-appengine-mail-api

require "uri"
require "net/http"

api_password = 'YOUR_API_PASSWORD'

url = URI("https://PROJECT_ID.REGION_ID.r.appspot.com/messages")

https = Net::HTTP.new(url.host, url.port)
https.use_ssl = true

request = Net::HTTP::Post.new(url)
request.basic_auth 'api', api_password
form_data = [
    ['to', 'test@nkn-it.de'],
    ['subject', 'Ruby Example'],
    ['text', 'This is a simple test.']
]
request.set_form form_data, 'multipart/form-data'
response = https.request(request)
puts response.read_body
