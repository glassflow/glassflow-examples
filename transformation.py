import json
import joblib
import numpy as np

# Load the pre-trained model (ensure this path is correct)
model = joblib.load("anomaly_detection_model.pkl")


def handler(data, log):
    """
    Detect anomalies in server logs using a pre-trained ML model.
    """
    log.info("Event received: " + json.dumps(data))

    # Preprocess the log data into the format expected by the model
    features = preprocess_log(data)

    # Predict the log status using the pre-trained model
    prediction = model.predict(features)

    # Update the mapping to work with the One-Class SVM output
    if prediction[0] == 1:
        status = "normal"
    else:
        status = "suspicious"

    # Return the status and log data
    return {"status": status, "log": data}


def preprocess_log(log):
    """
    Preprocess the log data into numerical features suitable for the model.
    """
    # Example preprocessing: Convert log attributes into numerical values
    # This will depend on your specific log format and feature engineering
    feature_vector = [
        len(log.get("message", "")),  # Length of the log message
        log.get("error_code", 0),  # Error code (if applicable)
        log.get("response_time", 0),  # Response time in ms
        log.get("status_code", 200),  # HTTP status code (default 200)
        log.get("user_id", 0),  # User ID (if applicable)
        len(log.get("user_agent", "")),  # Length of user agent string
        int(log.get("is_error", False)),  # Boolean if the log is an error (1 or 0)
        len(log.get("request_path", "")),  # Length of the request path
        log.get("request_size", 0),  # Size of the request (if applicable)
        log.get("response_size", 0),  # Size of the response (if applicable)
        int(
            log.get("is_cached", False)
        ),  # Boolean if the response was served from cache
        log.get("num_queries", 0),  # Number of database queries involved
        log.get("processing_time", 0),  # Processing time on the server side
    ]

    return np.array([feature_vector])


class MockLogger:
    def info(self, message):
        print("INFO:", message)


# Sample log data
sample_log = {
    "message": "User successfully logged in.",
    "error_code": 0,
    "response_time": 85,
    "status_code": 200,
    "user_id": 12345,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "is_error": False,
    "request_path": "/api/login",
    "request_size": 256,
    "response_size": 512,
    "is_cached": True,
    "num_queries": 1,
    "processing_time": 50,
}

# Create a mock logger instance
mock_logger = MockLogger()

# Call the handler function with the sample log
result = handler(sample_log, mock_logger)

# Output the result
print("Result:", result)
