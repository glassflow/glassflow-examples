from dotenv import load_dotenv
import glassflow
import json
import os
import sys


def send_message_to_glassflow(request_body, glassflow_client):
    response = glassflow_client.publish(request_body=request_body)
    if response.status_code == 200:
        print("Sent message to GlassFlow with ad ID:", request_body["id"])
    else:
        print(f"Failed to send data to GlassFlow: {response.text}")


def get_ads_data(path):
    for file in os.listdir(path):
        if file.endswith(".json"):
            print("Loading data from file:", file)
            data = json.load(open(path + file, "r"))
            for x in data:
                yield x


def main(data_path: str):
    pipeline_id = os.environ["PIPELINE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

    for ad in get_ads_data(data_path):
        send_message_to_glassflow(ad, glassflow_client)


if __name__ == "__main__":
    load_dotenv()
    main(data_path=sys.argv[1])
