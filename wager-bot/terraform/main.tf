data "google_project" "project" {
  project_id = "wager-bot-399722"
}


resource "google_cloud_scheduler_job" "default" {
  name     = "odds-api-daily"
  schedule = "0 14 * * * "
  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.function.url
    body        = base64encode("{\"name \":\"Hello World\"}")
    oidc_token {
      service_account_email = "${data.google_project.project.number}-compute@developer.gserviceaccount.com"
      audience              = "https://us-central1-wager-bot-399722.cloudfunctions.net/function-1"
    }
  }
  retry_config {
    retry_count = 1
  }
}



resource "google_secret_manager_secret" "default" {
  for_each = toset([
    "sports-odds-api-key",
    "wager-bot-discord-token"
  ])

  project   = data.google_project.project.number
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
    service_account_email            = "${data.google_project.project.number}-compute@developer.gserviceaccount.com"
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

resource "google_compute_region_instance_template" "wager-bot" {
  name         = "wager-bot"
  machine_type = "e2-micro"
  project      = "wager-bot-399722"
  region       = "us-east1"
  metadata = {
    "startup-script" = <<-EOT
            sudo adduser wager-bot
            sudo su wager-bot
            cd /home/wager-bot
            sudo apt update
            sudo apt-get -y upgrade
            sudo apt install -y python3-pip
            git clone https://github.com/adequevedo/dodona.git
            cd dodona/wager-bot/code/bot
            pip3 install -r requirements.txt
            python3 bot.py
        EOT
  }

  tags = [
    "http-server",
    "https-server",
  ]

  disk {
    auto_delete  = true
    boot         = true
    disk_size_gb = 10
    disk_type    = "pd-standard"
    source_image = "ubuntu-os-cloud/ubuntu-2204-jammy-v20231030"
    type         = "PERSISTENT"
  }

  network_interface {
    network = "default"

    access_config {
      network_tier = "PREMIUM"
    }
  }

  reservation_affinity {
    type = "ANY_RESERVATION"
  }

  scheduling {
    automatic_restart   = true
    min_node_cpus       = 0
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email = "bot-account@wager-bot-399722.iam.gserviceaccount.com"
    scopes = [
      "cloud-platform",
    ]
  }

}

resource "google_compute_instance_from_template" "tpl" {
  name = "wager-bot"
  zone = "us-east1-b"

  source_instance_template = google_compute_region_instance_template.wager-bot.self_link

}

resource "google_compute_resource_policy" "default" {
  name    = "wager-bot"
  project = trim(data.google_project.project.id, "projects/")
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

resource "random_id" "bucket_prefix" {
  byte_length = 8
}

resource "google_storage_bucket" "tf_state" {
  name          = "${random_id.bucket_prefix.hex}-bucket-tfstate"
  force_destroy = false
  location      = "US"
  storage_class = "STANDARD"
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "bucket" {
  name     = "dione"
  location = "us-east1"
}

# TODO 
# service agent acct perms 
# make bot service account w/ secret manager access 


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
