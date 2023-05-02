<?php

# Send email via Mail API
# https://github.com/Cyclenerd/google-cloud-appengine-mail-api
#
# Guzzle 7
# https://docs.guzzlephp.org/en/stable/overview.html#installation

require 'vendor/autoload.php';

$api_password = 'YOUR_API_PASSWORD';

$api_url = 'https://PROJECT_ID.REGION_ID.r.appspot.com/messages';

$client = new \GuzzleHttp\Client();
$response = $client->request('POST', $api_url, [
  'auth' => ['api', $api_password],
  'form_params' => [
    'to'      => 'test@nkn-it.de',
    'subject' => 'PHP Example',
    'text'    => 'This is a simple test.',
  ]
]);

echo $response->getBody();
