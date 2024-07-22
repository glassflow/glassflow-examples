import os
import json
import asyncio
from dotenv import load_dotenv
import nats
import glassflow


class NatsJetstreamSourceConnector:
    def __init__(
        self,
        nats_jetsream_subjects,
        glassflow_client,
    ):
        self.glassflow_client = glassflow_client
        self.nats_subject = nats_jetsream_subjects
        self.loop = asyncio.get_event_loop()

    async def on_event(self, msg):
        event_data_json = json.loads(
            msg.data.decode("utf-8")
        )
        response = self.glassflow_client.publish(
            request_body=event_data_json
        )
        if response.status_code == 200:
            print(
                "Data sent successfully to GlassFlow"
            )
            await msg.ack()
        else:
            print(
                f"Failed to send data to GlassFlow: {response.text}"
            )

    async def receive(self, js):
        await js.subscribe(
            self.nats_subject, cb=self.on_event
        )


async def main():
    # Load environment variables
    load_dotenv()

    pipeline_id = os.getenv("PIPELINE_ID")
    pipeline_access_token = os.getenv(
        "PIPELINE_ACCESS_TOKEN"
    )
    nats_jetsream_url = os.getenv(
        "NATS_JETSREAM_URL"
    )
    nats_jetsream_subjects = os.getenv(
        "NATS_JETSREAM_SUBJECTS"
    )

    # Initialize the GlassFlow client
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

    # Initialize the NATS Jetstream
    nc = await nats.connect(nats_jetsream_url)
    print(
        f"Connected to NATS at {nc.connected_url.netloc}..."
    )
    js = nc.jetstream()

    # Initialize the NatsJetsream source connector with the GlassFlow client
    nats_connector = NatsJetstreamSourceConnector(
        nats_jetsream_subjects, glassflow_client
    )

    # Start receiving events
    while True:
        await nats_connector.receive(js)


if __name__ == "__main__":
    asyncio.run(main())
