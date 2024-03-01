"""Get transformed data and store it locally on disk
alternate, push it to cloud storage bucket ?
alternate, push it to a realtime database
"""
import glassflow
import sys
import time
from dotenv import dotenv_values
import json


def main():
    config = dotenv_values(".env")
    print(config)
    pipeline_id = config.get("PIPELINE_ID")
    space_id = config.get("SPACE_ID")
    pipeline_access_token = config.get("PIPELINE_ACCESS_TOKEN")
    print("pipeline ID", pipeline_id)
    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(space_id=space_id,
                                             pipeline_id=pipeline_id)

    with open("mobility_data_transformed.txt", "a+") as f:
        while True:
            try:
                # consume transfornmed data from the pipeline
                res = pipeline_client.consume(
                    pipeline_access_token=pipeline_access_token)
                if res.status_code == 200:
                    # get the transformed data as json
                    data = res.body.event
                    print("Data consumed successfully")
                    print(data)
                    f.write(json.dumps(data) + "\n")
            except KeyboardInterrupt:
                print("exiting")
                sys.exit(0)
            time.sleep(0.5)


main()
