import os
import json
import asyncio
from dotenv import load_dotenv
import nats
import glassflow

class PostgreSQLSourceConnector:
    def __init__(self, glassflow_client):
        self.glassflow_client = glassflow_client
        self.nats_subject = "postgres.*.*"
        self.loop = asyncio.get_event_loop()

    async def on_event(self, msg):
        event_data_json = json.loads(msg.data.decode('utf-8'))
        response = self.glassflow_client.publish(request_body=event_data_json)
        if response.status_code == 200:
            print("Data sent successfully to GlassFlow")
        else:
            print(f"Failed to send data to GlassFlow: {response.text}")

    async def receive(self, js):
        await js.subscribe(self.nats_subject, cb=self.on_event)


async def main():
    # Load environment variables
    load_dotenv()

    # Initialize the GlassFlow client
    pipeline_id = os.getenv("PIPELINE_ID")
    space_id = os.getenv("SPACE_ID")
    pipeline_access_token = os.getenv("PIPELINE_ACCESS_TOKEN")
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        space_id=space_id,
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

    # Initialize the PostgreSQL source connector with the GlassFlow client
    pg_connector = PostgreSQLSourceConnector(glassflow_client)

    # Initialize the NATS Jetstream
    nc = await nats.connect("nats://nats:4222")
    print(f"Connected to NATS at {nc.connected_url.netloc}...")
    js = nc.jetstream()
    
    # Start receiving events
    while True:
        await pg_connector.receive(js)

if __name__ == "__main__":
    asyncio.run(main())
