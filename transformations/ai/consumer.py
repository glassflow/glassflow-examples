"""Get transformed data and store it locally on disk"""

import glassflow
import sys
from dotenv import dotenv_values
import json


def main():
    config = dotenv_values(".env")
    print(config)
    pipeline_id = config.get("PIPELINE_ID")
    space_id = config.get("SPACE_ID")
    token = config.get("PIPELINE_ACCESS_TOKEN")

    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(
        space_id=space_id, pipeline_id=pipeline_id, pipeline_access_token=token
    )

    with open("output_logs.txt", "a+") as f:
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
                print("exiting")
                sys.exit(0)


if __name__ == "__main__":
    main()
