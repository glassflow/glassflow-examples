# consumer.py

import glassflow
import json
import sys


def read_data_from_pipeline(file_path):
    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client()

    with open(file_path, "a+") as f:
        while True:
            try:
                # consume transfornmed data from the pipeline
                res = pipeline_client.consume()
                if res.status_code == 200:
                    # get the transformed data as json
                    data = res.body.event
                    print("Data consumed successfully")
                    print(data)
                    f.write(json.dumps(data) + "\n")
                    f.flush()
            except KeyboardInterrupt:
                print("Exiting program")
                sys.exit(0)


if __name__ == "__main__":
    read_data_from_pipeline("supplier_inventory.txt")
