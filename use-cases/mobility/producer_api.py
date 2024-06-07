"""
Get mobility events data via a mockserver and publish it to glassflow
"""
import glassflow
from dotenv import dotenv_values
import requests


def get_mock_events():
    """
    Get mock events from the mock server
    """
    res = requests.get(
        "https://mock-mobility-s3r3lbzina-ey.a.run.app/mobility/producer/events/ride-completed"
    )
    if res.status_code == 200:
        return res.json()
    else:
        print("Failed to get mock events")
        return None


def main():
    config = dotenv_values(".env")
    pipeline_id = config.get("PIPELINE_ID")
    space_id = config.get("SPACE_ID")
    token = config.get("PIPELINE_ACCESS_TOKEN")

    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(space_id=space_id,
                                             pipeline_id=pipeline_id,
                                             pipeline_access_token=token)
    counter = 0
    while True and counter < 1000:
        try:
            event = get_mock_events()
            counter += 1
            if event:
                req = pipeline_client.publish(request_body=event[0])

                if req.status_code == 200:
                    print("Event published successfully", event[0])
                else:
                    print("Failed to publish event")
                    print(req.text)
        except Exception as e:
            print(e)
            break
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
