"""
Generate mobility events data and publish it to glassflow
"""
import glassflow
from time import sleep
import sys
from dotenv import dotenv_values
from utils.dataproducer import DataProducer


def main():
    config = dotenv_values(".env")
    pipeline_id = config.get("PIPELINE_ID")
    space_id = config.get("SPACE_ID")
    pipeline_access_token = config.get("PIPELINE_ACCESS_TOKEN")
    print("pipeline ID", pipeline_id)
    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(space_id=space_id,
                                             pipeline_id=pipeline_id)
    dp = DataProducer("mobility")
    while True:
        try:
            event = dp.ride_completed()
            req = pipeline_client.publish(
                request_body=event,
                pipeline_access_token=pipeline_access_token)
            if req.status_code == 200:
                print("Event published successfully")
            else:
                print("Failed to publish event")
                print(req.text)
            sleep(0.5)
        except Exception as e:
            print(e)
            break
        except KeyboardInterrupt:
            break


main()
