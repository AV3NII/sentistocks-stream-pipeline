# Define environment variables
$PROJECT_NAME = "sentistocks" 
$PROJECT_ID = "sentistocks-22345"  
$SERVICE_ACCOUNT_NAME = "terra-runner-sentistocks" 
$BILLING_ACCOUNT_ID = "xxxxxxxxxx"    #    <---------- INSERT YOUR BILLING ACCOUNT ID HERE
$KEY_PATH = "./secrets/gcp-sentistocks-credentials.json" 

# Authenticate with gcloud
gcloud auth login

# Create a new project
gcloud projects create $PROJECT_ID --name=$PROJECT_NAME
Write-Host "Project $PROJECT_NAME created."

# Link project to the billing account
gcloud alpha billing projects link $PROJECT_ID --billing-account=$BILLING_ACCOUNT_ID
Write-Host "Project $PROJECT_ID linked to billing account $BILLING_ACCOUNT_ID."

# Set the project to be the current project
gcloud config set project $PROJECT_ID

# Create a service account
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME `
    --description="Service account for BigQuery access" `
    --display-name="SentiStocks Service Account"
Write-Host "Service account $SERVICE_ACCOUNT_NAME created."


gcloud projects add-iam-policy-binding $PROJECT_ID `
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" `
    --role="roles/bigquery.admin"
Write-Host "BigQuery Administrator role granted to $SERVICE_ACCOUNT_NAME."


# Create and download the service account key
gcloud iam service-accounts keys create $KEY_PATH `
    --iam-account "${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
Write-Host "Service account key created and downloaded to $KEY_PATH."

# Activate the service account with gcloud
gcloud auth activate-service-account --key-file=$KEY_PATH
Write-Host "Service account activated in gcloud configuration."

Write-Host "Setup complete. You're now using your service account with gcloud."
