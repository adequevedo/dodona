resource "google_cloud_scheduler_job" "default" {
  name     = "odds-api-daily"
  schedule = "0 14 * * * "
  http_target {
    http_method = "POST"
    uri         = "https://us-central1-wager-bot-399722.cloudfunctions.net/function-1"
    body        = base64encode("{\"name \":\"Hello World\"}")
    oidc_token {
      service_account_email = "371661757130-compute@developer.gserviceaccount.com"
      audience              = "https://us-central1-wager-bot-399722.cloudfunctions.net/function-1"
    }
  }
  retry_config {
    retry_count = 1
  }
}

resource "google_storage_bucket" "bucket" {
  name     = "dione"
  location = "us-east1"
}

resource "google_secret_manager_secret" "default" {
  for_each = toset([
    "sports-odds-api-key",
    "wager-bot-discord-token"
  ])

  project   = "371661757130"
  secret_id = each.key

  replication {
    auto {
    }
  }

  timeouts {}
}


resource "google_cloudfunctions2_function" "function" {

  location = "us-central1"
  name     = "function-1"
  project  = "wager-bot-399722"

  build_config {
    entry_point           = "hello_http"
    environment_variables = {}
    runtime               = "python311"

    source {
      storage_source {
        bucket = "gcf-v2-sources-371661757130-us-central1"
        object = "function-1/function-source.zip"
      }
    }
  }

  service_config {
    all_traffic_on_latest_revision   = true
    available_cpu                    = "83m"
    available_memory                 = "128Mi"
    environment_variables            = {}
    ingress_settings                 = "ALLOW_ALL"
    max_instance_count               = 59
    max_instance_request_concurrency = 1
    min_instance_count               = 0
    service_account_email            = "371661757130-compute@developer.gserviceaccount.com"
    timeout_seconds                  = 60

    secret_environment_variables {
      key        = "API_KEY"
      project_id = "wager-bot-399722"
      secret     = element(local.secret_name, length(local.secret_name) - 1)
      version    = "1"
    }
  }

  timeouts {}
}

locals {
  secret_name = split("/", google_secret_manager_secret.default["sports-odds-api-key"].name, )
}


resource "google_compute_instance" "default" {

  machine_type = "e2-micro"
  metadata = {
    "startup-script" = <<-EOT
            whoami
            sudo su alexdequevedo
            whoami
            cd /home/alexdequevedo/bot
            pip3 install -r requirements.txt
            python3 bot.py
        EOT
  }
  name    = "dione"
  project = "wager-bot-399722"

  tags = [
    "http-server",
    "https-server",
  ]
  zone = "us-east1-b"

  boot_disk {
    auto_delete = true

    initialize_params {
      image = "ubuntu-2004-focal-v20230918"
      size  = 10
      type  = "pd-standard"
    }
  }


  service_account {
    email = "371661757130-compute@developer.gserviceaccount.com"
    scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring.write",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/trace.append",
    ]
  }

  network_interface {
    network = "default"

    access_config {
      network_tier = "STANDARD"
    }
  }


  scheduling {
    preemptible       = true
    automatic_restart = false
  }
  resource_policies = [google_compute_resource_policy.default.id]

  timeouts {}
  lifecycle {
    ignore_changes = [
      metadata
    ]
  }
}


resource "google_compute_resource_policy" "default" {
  name    = "wager-bot"
  project = "wager-bot-399722"
  region  = "us-east1"

  instance_schedule_policy {
    time_zone = "America/New_York"

    vm_start_schedule {
      schedule = "0 7 * * *"
    }

    vm_stop_schedule {
      schedule = "0 0 * * *"
    }
  }
}

# Enable APIs

# resource "google_project_service" "project" {
#   for_each = toset([
#     "iam.googleapis.com",
#     "storage.googleapis.com",
#     "cloudresourcemanager.googleapis.com",
#     "compute.googleapis.com",
#     "servicecontrol.googleapis.com",
#   ])

#   project = var.project_id
#   service = each.key

#   timeouts {
#     create = "30m"
#     update = "40m"
#   }

#   disable_dependent_services = true
# }



# ##################################################
# Backend Service Account
# ##################################################

# resource "google_service_account" "backend_service_account" {
#   project      = var.project_id
#   account_id   = "employees-backend-sa"
#   display_name = "employees-backend-sa"
#   description  = "Service account for Amazing Employees Backend"

#   depends_on = [
#     google_project_service.project["cloudresourcemanager.googleapis.com"],
#     google_project_service.project["iam.googleapis.com"],
#     google_project_service.project["compute.googleapis.com"],
#   ]
# }

# resource "google_project_iam_member" "backend_iam_member" {
#   project = var.project_id
#   role    = "roles/datastore.user"
#   member  = "serviceAccount:${google_service_account.backend_service_account.email}"

#   depends_on = [
#     google_project_service.project["cloudresourcemanager.googleapis.com"],
#     google_project_service.project["iam.googleapis.com"],
#     google_project_service.project["compute.googleapis.com"],
#   ]
# }