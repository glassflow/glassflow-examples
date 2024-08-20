import openai
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_distances

openai.api_key = "your_open_api_key"

# Set a predefined threshold for anomaly detection
ANOMALY_THRESHOLD = 0.8  # You may need to adjust this based on your data


def handler(data, log):
    """
    Generate AI insights, detect anomalies and transform server logs data.
    """
    log.info("Event:" + json.dumps(data), data=data)

    insights = detect_anomalies(data)
    return insights


def detect_anomalies(log):
    # Convert log data to a string format
    log_text = json.dumps(log)

    # Generate embedding for the log using OpenAI's embedding endpoint
    response = openai.embeddings.create(input=log_text, model="text-embedding-3-small")
    embedding = response.data[0].embedding

    # Example: You might compare the log embedding to a predefined set of normal log embeddings
    # For simplicity, let's assume you have a list of normal log embeddings
    normal_log_embeddings = [
        # Example embeddings for normal logs (these should be generated from actual normal logs)
        [0.01, 0.02, 0.03, ..., 0.04],  # Replace with real embeddings
        [0.05, 0.06, 0.07, ..., 0.08],
        # Add more normal log embeddings
    ]

    if normal_log_embeddings:
        # Calculate the cosine distance between the log embedding and normal log embeddings
        distances = cosine_distances([embedding], normal_log_embeddings)
        min_distance = np.min(distances)
    else:
        # If no normal embeddings are available, classify all as normal initially
        min_distance = 0

    # Classify the log based on the distance
    if min_distance > ANOMALY_THRESHOLD:
        status = "suspicious"
    else:
        status = "normal"

    # Return the insights in JSON format
    insights = {"status": status, "log": log}

    return insights


# Sample input log data
sample_log_data = {
    "timestamp": "2024-08-12T14:30:00Z",
    "level": "INFO",
    "message": "User logged in",
    "user_id": "12345",
    "ip_address": "192.168.1.1",
    "request_url": "/login",
    "response_code": 200,
    "response_time_ms": 150,
}

# Example usage of the handler function
if __name__ == "__main__":

    class Logger:
        @staticmethod
        def info(message, data=None):
            print(message)

    log = Logger()
    result = handler(sample_log_data, log)
    print("Result:", json.dumps(result, indent=2))
