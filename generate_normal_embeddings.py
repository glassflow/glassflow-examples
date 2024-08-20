import openai
import json

openai.api_key = "your_open_api_key"

# Step 1: Prepare Sample Normal Log Data
normal_logs = [
    {
        "timestamp": "2024-08-12T14:30:00Z",
        "level": "INFO",
        "message": "User logged in",
        "user_id": "12345",
        "ip_address": "192.168.1.1",
        "request_url": "/login",
        "response_code": 200,
        "response_time_ms": 150,
    },
    {
        "timestamp": "2024-08-12T14:31:00Z",
        "level": "INFO",
        "message": "User accessed dashboard",
        "user_id": "12345",
        "ip_address": "192.168.1.1",
        "request_url": "/dashboard",
        "response_code": 200,
        "response_time_ms": 120,
    },
    # Add more normal log samples as needed
]

# Step 2: Generate Embeddings for Each Log
normal_log_embeddings = []

for log in normal_logs:
    log_text = json.dumps(log)
    response = openai.embeddings.create(input=log_text, model="text-embedding-ada-002")
    embedding = response.data[0].embedding
    normal_log_embeddings.append(embedding)

# Step 3: Store These Embeddings
print("Normal Log Embeddings:")
for i, embedding in enumerate(normal_log_embeddings):
    print(f"Log {i+1} Embedding: {embedding}")

# Now you can use the `normal_log_embeddings` in your anomaly detection logic
