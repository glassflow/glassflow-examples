import os
import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
import glassflow
from dotenv import load_dotenv
import json


class EventHubSourceConnector:
    def __init__(self, glassflow_client):
        self.connection_str = os.getenv("AZURE_EVENT_HUB_CONNECTION_STRING")
        self.consumer_group = os.getenv("AZURE_EVENT_HUB_CONSUMER_GROUP")
        self.eventhub_name = os.getenv("AZURE_EVENT_HUB_NAME")
        self.setup_source()
        self.glassflow_client = glassflow_client

    def setup_source(self):
        self.checkpoint_store = BlobCheckpointStore.from_connection_string(
            os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
            os.getenv("AZURE_STORAGE_BLOB_CONTAINER_NAME"),
        )
        self.consumer_client = EventHubConsumerClient.from_connection_string(
            self.connection_str,
            consumer_group=self.consumer_group,
            eventhub_name=self.eventhub_name,
            checkpoint_store=self.checkpoint_store,
        )

    async def on_event(self, partition_context, event):
        print(
            'Received the event: "{}" from the Event Hubs partition with ID: "{}"'.format(
                event.body_as_str(), partition_context.partition_id
            )
        )

        await partition_context.update_checkpoint(event)

        # Send each event to GlassFlow
        event_data_json = json.loads(event.body_as_str())
        response = self.glassflow_client.publish(request_body=event_data_json)
        if response.status_code == 200:
            print("Data sent successfully to GlassFlow")
        else:
            print(f"Failed to send data to GlassFlow: {response.text}")

    async def receive(self):
        await self.consumer_client.receive(
            on_event=self.on_event, starting_position="-1"
        )


async def main():
    # Initialize the glassflow client
    pipeline_id = os.environ["PIPELINE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

    # Initialize the Event Hub source connector with the GlassFlow client
    eventhub_connector = EventHubSourceConnector(glassflow_client)

    # Start receiving events
    await eventhub_connector.receive()


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
