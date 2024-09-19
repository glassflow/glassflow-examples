import glassflow
import sys
import time
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

project_id = config.get("PROJECT_ID")
subscription_id = config.get("SUBSCRIPTION_ID")
pipeline_id = config.get("PIPELINE_ID")
token = config.get("PIPELINE_ACCESS_TOKEN")


def read_data_from_pipeline(file_path):
    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(pipeline_id=pipeline_id,
                                             pipeline_access_token=token)

    with open(file_path, "a+") as f:
        while True:
            try:
                print("Consuming data from GlassFlow pipeline...")
                # consume transformed data from the pipeline
                res = pipeline_client.consume()
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


read_data_from_pipeline("ecommerce-orders.txt")