import json
import requests

# Your Azure ML endpoint
scoring_uri = "YOUR_AZURE_ML_ENDPOINT"
api_key = "YOUR_AZURE_ML_API_KEY"  # Optional if your endpoint is secured


def call_azure_ml(data):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Prepare the data in the format the model expects
    input_data = {"data": [data]}

    # Make the API request
    response = requests.post(scoring_uri, json=input_data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}


def handler(data, log):
    """
    Detect anomalies using an Azure ML model.
    """
    log.info("Event received: " + json.dumps(data))

    # Call the Azure ML model
    ml_response = call_azure_ml(data)

    # Process the response
    if "error" not in ml_response:
        log.info(f"Model response: {ml_response}")
        return ml_response
    else:
        log.error(f"Failed to get a response from the model: {ml_response['error']}")
        return {"error": "Model inference failed"}
