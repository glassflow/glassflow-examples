from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import glassflow
import json
from dotenv import dotenv_values

config = dotenv_values(".env")
project_id = config.get("PROJECT_ID")
subscription_id = config.get("SUBSCRIPTION_ID")
pipeline_id = config.get("PIPELINE_ID")
space_id = config.get("SPACE_ID")
pipeline_access_token = config.get("PIPELINE_ACCESS_TOKEN")
# Number of seconds the subscriber should listen for messages
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

client = glassflow.GlassFlowClient()
pipeline_client = client.pipeline_client(space_id=space_id, pipeline_id=pipeline_id)


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received message: {message}.")

    data = json.loads(message.data.decode("utf-8"))

    # Here you can transform or directly send the data to GlassFlow
    # For example, let's send the data directly
    try:
        # Publish the data to the GlassFlow pipeline
        response = pipeline_client.publish(
            request_body=data, pipeline_access_token=pipeline_access_token
        )
        if response.status_code == 200:
            print("Data sent successfully to GlassFlow.")
        else:
            print(f"Failed to send data to GlassFlow: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Acknowledge the message so it's not sent again
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
