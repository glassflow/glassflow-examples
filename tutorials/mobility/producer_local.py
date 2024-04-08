"""
Generate mobility events data and publish it to glassflow
"""
import glassflow
from time import sleep
from dotenv import dotenv_values
from utils.dataproducer import DataProducer


def main():
    config = dotenv_values(".env")
    pipeline_id = config.get("PIPELINE_ID")
    space_id = config.get("SPACE_ID")
    token = config.get("PIPELINE_ACCESS_TOKEN")
    
    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(space_id=space_id,
                                             pipeline_id=pipeline_id,
                                             pipeline_access_token=token)
    dp = DataProducer("mobility")
    while True:
        try:
            event = dp.ride_completed()
            req = pipeline_client.publish(request_body=event)
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
