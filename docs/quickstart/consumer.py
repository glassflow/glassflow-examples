import glassflow
from dotenv import dotenv_values
import json


def read_data_from_pipeline(file_path):
    config = dotenv_values(".env")
    pipeline_id = config.get("PIPELINE_ID")
    space_id = config.get("SPACE_ID")
    token = config.get("PIPELINE_ACCESS_TOKEN")

    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(
        space_id=space_id, pipeline_id=pipeline_id, pipeline_access_token=token
    )

    try:
        while True:
            # consume transformed data from the pipeline
            res = pipeline_client.consume()

            if res.status_code == 200:
                # get the transformed data as json
                data = res.body.event
                print("Data consumed successfully")
                print(data)
                with open(file_path, "a+") as f:
                    f.write(json.dumps(data) + "\n")
                    f.flush()
    except KeyboardInterrupt:
        print("Exiting program")


if __name__ == "__main__":
    read_data_from_pipeline("supplier_inventory.txt")
