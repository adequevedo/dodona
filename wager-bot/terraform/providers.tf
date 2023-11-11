terraform {
  required_providers {
    google = {
      source = "hashicorp/google-beta"
    }
  }
  backend "gcs" {
    bucket = "fff081dee416cf26-bucket-tfstate"
    prefix = "terraform/wager-bot"
  }
}

provider "google" {
  project = var.project_id
  region  = "us-east1"
}

