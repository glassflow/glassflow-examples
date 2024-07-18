from dotenv import load_dotenv
import glassflow
import os
import base64


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

    ads = [
        {
            "id": "rdfcw4a53a",
            "user_id": "54qf4323623",
            "title": "Math tutor for high school",
            "description": "I amd a Math graduate and graduated with honors in the university of Barcelona"
                           "I can give you theoretical classes and practical labs where we go through problems"
                           "and their solutions",
        },
        {
            "id": "rdfcw4a53a",
            "user_id": "54qf4323623",
            "title": "I sell almost new cabinet",
            "description": """
                    The cabinet is made of oak wood
                    dimensions: 100x80x40
                    """,
            "images": [
                {
                    "format": "image/jpg",
                    "b64": encode_image("ad_image1.jpg")
                }
            ]
        }
    ]

    for ad in ads:
        send_message_to_glassflow(ad, glassflow_client)


if __name__ == "__main__":
    load_dotenv()
    main()
