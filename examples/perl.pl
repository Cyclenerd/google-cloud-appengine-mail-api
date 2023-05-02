#!/usr/bin/perl

# Send email via Mail API
# https://github.com/Cyclenerd/google-cloud-appengine-mail-api

use strict;
use LWP::UserAgent;
use HTTP::Request::Common;

my $api_password = 'YOUR_API_PASSWORD';

my $url = 'https://PROJECT_ID.REGION_ID.r.appspot.com/messages';

my $ua = LWP::UserAgent->new;
my $request = POST "$url", [
	to      => 'test@nkn-it.de',
	subject => 'Perl Example',
	text    => 'This is a simple test.',
];
$request->authorization_basic("api", $api_password);
my $response = $ua->request($request);

if ($response->is_success) {
	print $response->decoded_content;
} else {
	die "ERROR: Mail could not be sent! Status: '". $response->status_line ."'\n";
}