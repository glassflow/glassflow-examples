import base64
import glassflow
import json
import os
from dotenv import load_dotenv


def encode_image(image_path: str):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')


def send_message_to_glassflow(request_body, glassflow_client):
    response = glassflow_client.publish(request_body=request_body)
    if response.status_code == 200:
        print("Message sent to GlassFlow:", request_body)
    else:
        print(f"Failed to send data to GlassFlow: {response.text}")


def main():
    # Initialize GlassFlow client
    pipeline_id = os.environ["PIPELINE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

    ads = json.load(open("data/classified-ads-examples.json", "r"))
    for ad in ads:
        # Read images and send them to the pipeline base64 encoded
        if "images" in ad and len(ad["images"]) > 0:
            images = []
            for img in ad["images"]:
                img_b64v = encode_image(img["path"])
                images.append(dict(format=img["format"], b64=img_b64v))
            ad["images"] = images

        send_message_to_glassflow(ad, glassflow_client)


if __name__ == "__main__":
    load_dotenv()
    main()
