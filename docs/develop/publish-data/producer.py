import glassflow
from dotenv import load_dotenv
import os

load_dotenv()

pipeline_id = os.getenv("PIPELINE_ID")
space_id = os.getenv("SPACE_ID")
token = os.getenv("PIPELINE_ACCESS_TOKEN")

# 1. Initializes a GlassFlow Python client
client = glassflow.GlassFlowClient()
# 2. Creates a pipeline
pipeline_client = client.pipeline_client(
    space_id=space_id, pipeline_id=pipeline_id, pipeline_access_token=token
)

# This can be any real-time data from any data sources
data = {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "model": "BMW",
    "year": 2020,
    "price": 20000,
    "transmission": "automatic",
    "mileage": 15000,
    "fuelType": "petrol",
    "tax": 150,
    "mpg": 35,
    "engineSize": 1.8,
}

# 3. Publishes a new event into the pipeline
response = pipeline_client.publish(request_body=data)
if response.status_code == 200:
    print("Data sent successfully to GlassFlow")
else:
    print(f"Failed to send data to GlassFlow: {response.text}")
