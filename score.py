import os
import joblib
import numpy as np
import json

# Global model variable
model = None


def init():
    """
    Initialize the model. This function is called once at the beginning
    to load the model into memory from the Azure ML directory.
    """
    global model
    # Get the path to the model directory
    model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "model/anomaly_detection_model.pkl"
    )
    # Load the trained model
    model = joblib.load(model_path)
    print("Model loaded successfully from:", model_path)


def run(raw_data):
    """
    Run the model inference. This function is called each time a new input
    needs to be scored.

    Parameters:
    - raw_data (str): The input data as a JSON string.

    Returns:
    - str: The scoring result as a JSON string.
    """
    try:
        # Parse the input data
        log_entry = json.loads(raw_data)
        log_entry = np.array(log_entry).reshape(1, -1)

        # Make prediction
        prediction = model.predict(log_entry)

        # Prepare the result
        if prediction == -1:
            result = {"status": "anomalous", "log": log_entry.tolist()}
        else:
            result = {"status": "normal", "log": log_entry.tolist()}

        # Return the result as a JSON string
        return json.dumps(result, indent=2)

    except Exception as e:
        error_message = f"Error during model inference: {str(e)}"
        return json.dumps({"error": error_message}, indent=2)
