


#############################################
###            BigQuery Resources         ###
#############################################

# Define BigQuery Dataset
#===========================================================================
resource "google_bigquery_dataset" "sentistocks_dataset" {
  dataset_id    = "coinbase"
  friendly_name = "Coinbase Dataset"
  description   = "This dataset stores the tables for the dashboard."
  location      = var.zone
  project       = local.project_id
  
  default_table_expiration_ms = 2592000000 # 30 days

  labels = {
    environment = "development"
  }
}

# Define BigQuery Tables
#===========================================================================

#   ---   (1) coinbase historical   -----------------
resource "google_bigquery_table" "histo" {
  dataset_id = google_bigquery_dataset.sentistocks_dataset.dataset_id
  table_id   = "histo"
  project    = local.project_id
  deletion_protection = false

  schema = jsonencode([
    {
      name = "Date",
      type = "DATETIME",
      mode = "REQUIRED"
    },
    {
      name = "Lowest_Price",
      type = "FLOAT",
      mode = "REQUIRED"
    },
    {
      name = "Highest_Price",
      type = "FLOAT",
      mode = "REQUIRED"
    },
    {
      name = "Opening_Price",
      type = "FLOAT",
      mode = "REQUIRED"
    },
    {
      name = "Closing_Price",
      type = "FLOAT",
      mode = "REQUIRED"
    },
    {
      name = "Volume_Traded",
      type = "FLOAT",
      mode = "REQUIRED"
    },
    {
      name = "Cryptocurrency",
      type = "STRING",
      mode = "REQUIRED"
    },
    {
      name = "Month",
      type = "INTEGER",
      mode = "REQUIRED"
    },
    {
      name = "Year",
      type = "INTEGER",
      mode = "REQUIRED"
    }
  ])
  
  labels = {
    environment = "development"
  }
}
