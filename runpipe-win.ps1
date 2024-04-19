
$uri = 'http://localhost:6789/api/pipeline_schedules/3/api_trigger'
$headers = @{
  
    'Content-Type' = 'application/json'
    'Authorization' = 'Bearer 82ef3658b20f44baa67ecb66aaf4643c'
}
  
# Use Invoke-WebRequest to send a POST request
$response = Invoke-WebRequest -Uri $uri -Method POST -Headers $headers -Body "{}"

# Optionally, display the response content
Write-Output $response.Content
