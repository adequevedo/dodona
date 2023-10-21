terraform {
  required_providers {
    google = {
      source = "hashicorp/google-beta"
    }
  }
}

provider "google" {
  project = "wager-bot-399722"
  region  = "us-central1"
}