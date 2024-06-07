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

# 3. Consumes a new event from the pipeline
response = pipeline_client.consume()
print(response)
if response.status_code == 200:
    data = response.json()
    print("Consumed Data:", data)
else:
    print(f"Failed to consume data from GlassFlow: {response.text}")
