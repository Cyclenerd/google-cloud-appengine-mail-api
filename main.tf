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

variable "project_id" {
  description = "The project ID"
  type        = string
  nullable    = false
}

variable "secret_id" {
  description = "The secret ID"
  type        = string
  nullable    = false
  default     = "api-password"
}

data "google_app_engine_default_service_account" "default" {
  project = var.project_id
}

resource "google_project_service" "secretmanager" {
  project            = var.project_id
  service            = "secretmanager.googleapis.com"
  disable_on_destroy = false
}

resource "google_secret_manager_secret" "api-password" {
  project   = var.project_id
  secret_id = var.secret_id
  replication {
    auto {}
  }
  depends_on = [google_project_service.secretmanager]
}

resource "google_secret_manager_secret_iam_member" "api-password-app-engine" {
  project    = var.project_id
  secret_id  = google_secret_manager_secret.api-password.secret_id
  role       = "roles/secretmanager.secretAccessor"
  member     = "serviceAccount:${data.google_app_engine_default_service_account.default.email}"
  depends_on = [google_secret_manager_secret.api-password]
}

output "secret_id" {
  value = google_secret_manager_secret.api-password.secret_id
}

output "app_engine_default_service_account" {
  value = data.google_app_engine_default_service_account.default.email
}