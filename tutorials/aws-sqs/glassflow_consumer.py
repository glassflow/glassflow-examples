import glassflow
import sys
import time
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

pipeline_id = config.get("PIPELINE_ID")
space_id = config.get("SPACE_ID")
pipeline_access_token = config.get("PIPELINE_ACCESS_TOKEN")


def read_data_from_pipeline(file_path):
    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(space_id=space_id, pipeline_id=pipeline_id)

    with open(file_path, "a+") as f:
        while True:
            try:
                print("Consuming data from GlassFlow pipeline...")
                res = pipeline_client.consume(
                    pipeline_access_token=pipeline_access_token
                )
                print(res)
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


read_data_from_pipeline("customer-feedback-analysis.txt")
