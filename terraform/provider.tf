provider "google" {
  project = "python-project-cluster"
  region = "us-central1"
}

terraform {
  backend "gcs" {
    bucket = "gcp-bucket-62"
    prefix = "terraform/state"
  }
  required_providers {
    google = {
        source = "hashicorp/google"
        version = "~>4.0"
    }
  }
}