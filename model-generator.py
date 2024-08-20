import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
from sklearn.metrics import classification_report
import joblib


# Generate some synthetic log data with additional features
def generate_log_data(n_samples=1000, anomaly_ratio=0.05):
    np.random.seed(42)
    n_anomalies = int(n_samples * anomaly_ratio)

    # Normal log entries
    normal_data = np.random.normal(loc=0, scale=1, size=(n_samples - n_anomalies, 13))

    # Anomalous log entries
    anomaly_data = np.random.normal(loc=4, scale=1, size=(n_anomalies, 13))

    data = np.vstack([normal_data, anomaly_data])
    labels = np.hstack([np.ones(n_samples - n_anomalies), -1 * np.ones(n_anomalies)])

    return data, labels


# Load or generate data
X, y = generate_log_data()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train a one-class SVM model
model = OneClassSVM(gamma="auto", nu=0.1)
model.fit(X_train)

# Save the trained model to a file
joblib.dump(model, "anomaly_detection_model.pkl")

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

print("Model training complete and saved as 'anomaly_detection_model.pkl'")
