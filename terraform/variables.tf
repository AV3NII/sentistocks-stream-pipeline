
variable "credentials" {
  description = "Path to the keyfile containing GCP credentials."
  type        = string
  default     = "../secrets/gcp-sentistocks-credentials.json"
}
variable "region" {
  type        = string
  description = "The default compute region"
  default     = "europe-west3"
}

variable "zone" {
  type        = string
  description = "The default compute zone"
  default     = "EU"
}
