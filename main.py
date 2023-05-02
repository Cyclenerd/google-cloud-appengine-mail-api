# Copyright 2023 Nils Knieling
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from google.appengine.api import mail
from google.appengine.api import wrap_wsgi_app
# Import the Secret Manager client library.
from google.cloud import secretmanager

app = Flask(__name__)
auth = HTTPBasicAuth()

# Enable access to bundled services
app.wsgi_app = wrap_wsgi_app(app.wsgi_app)

# Get Google Cloud project ID
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
# Get mail sender (email address for From header)
mail_sender = os.environ.get("SENDER") if os.environ.get("SENDER") \
    else f"{project_id} <no-reply@{project_id}.appspotmail.com>"


@auth.verify_password
def verify_password(username, password):
    if username != "api":
        error_log = {
            "severity": "NOTICE",
            "message": f"Unknown username '{username}'"
        }
        print(json.dumps(error_log))
        return None

    # Get secret ID
    secret_id = os.environ.get("SECRET_ID")
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    request = {"name": f"projects/{project_id}/secrets/{secret_id}/versions/latest"}
    # Get the secret.
    try:
        response = client.access_secret_version(request)
    except Exception as e:
        error_log = {
            "severity": "ALERT",
            "message": f"Accessing the secret ID '{secret_id}' failed with exception {e}."
        }
        print(json.dumps(error_log))
        return False

    secret_payload = response.payload.data.decode("UTF-8")
    secret_payload_hash = generate_password_hash(secret_payload)
    if check_password_hash(secret_payload_hash, password):
        return username


@app.route("/", methods=["GET"])
@auth.login_required
def root():
    return "Mail API"


@app.route("/messages", methods=["POST"])
@auth.login_required
def messages():
    mail_to = request.form.get("to")
    if mail_to is None:
        error_log = {
            "severity": "WARNING",
            "message": "Missing to address"
        }
        print(json.dumps(error_log))
        return "Error: Missing to address", 400

    mail_subject = request.form.get("subject")
    if mail_subject is None:
        error_log = {
            "severity": "WARNING",
            "message": "Missing subject"
        }
        print(json.dumps(error_log))
        return "Error: Missing subject", 400

    mail_body = request.form.get("text")
    if mail_body is None:
        error_log = {
            "severity": "WARNING",
            "message": "Missing text"
        }
        print(json.dumps(error_log))
        return "Error: Missing text", 400

    try:
        mail.send_mail(
            sender=mail_sender,
            to=mail_to,
            subject=mail_subject,
            body=mail_body,
        )
    except Exception as e:
        error_log = {
            "severity": "ERROR",
            "message": f"Sending mail from '{mail_sender}' to '{mail_to}' failed with exception {e}."
        }
        print(json.dumps(error_log))
        return f"Exception {e} when sending mail from {mail_sender} to {mail_to}.", 500

    log_entry = {
        "severity": "INFO",
        "message": f"Successfully sent mail to '{mail_to}'."
    }
    print(json.dumps(log_entry))
    return f"Successfully sent mail to {mail_to}.", 201
