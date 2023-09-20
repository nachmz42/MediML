import json
import os

# Get environment variables
gcp_service_name = os.getenv('GCP_SERVICE_NAME')
gcp_region = os.getenv('GCP_LOCAL_REGION')

# Create a dictionary with the configuration
config = {
    "hosting": {
        "rewrites": [
            {
                "source": "**",
                "run": {
                    "serviceId": gcp_service_name,
                    "region": gcp_region
                }
            }
        ]
    }
}

# Convert the dictionary to a JSON string with indentation
config_json = json.dumps(config, indent=2)

# Write the JSON string to a file
with open('firebase.json', 'w') as config_file:
    config_file.write(config_json)
