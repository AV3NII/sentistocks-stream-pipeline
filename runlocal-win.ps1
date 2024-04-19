
$CREDENTIALS_FILE = "./secrets/gcp-sentistocks-credentials.json"

$PROJECT_ID = (Get-Content $CREDENTIALS_FILE | ConvertFrom-Json).project_id

# Export the PROJECT_ID so it's available to docker-compose as an environment variable
[Environment]::SetEnvironmentVariable("PROJECT_ID", $PROJECT_ID, "Process")

docker-compose up
