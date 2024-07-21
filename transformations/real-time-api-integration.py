import json
import requests
import pandas as pd
import joblib
from datetime import datetime

model = joblib.load("model.pkl")


def handler(data, log):
    log.info("Event:" + json.dumps(data), data=data)

    data["timestamp"] = datetime.utcnow().isoformat()

    # Real-time API integration for external factors
    weather_response = requests.get(
        f"https://api.weatherapi.com/v1/current.json?key=your_api_key&q={data['location']}"
    )
    weather = weather_response.json()["current"]["condition"]["text"]
    data["weather"] = weather

    # Apply predictive maintenance model
    sensor_data = pd.DataFrame([data["sensor_readings"]])
    failure_risk = predict_failure_risk(sensor_data)
    data["failure_risk"] = failure_risk

    return data


def predict_failure_risk(sensor_data):
    # Use the loaded model to predict failure risk
    prediction = model.predict(sensor_data)
    return "high" if prediction[0] == 1 else "low"
