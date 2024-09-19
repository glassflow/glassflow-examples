import glassflow
import sys
from dotenv import load_dotenv
import os


def main():
    pipeline_id = os.environ["PIPELINE_ID"]
    token = os.environ["PIPELINE_ACCESS_TOKEN"]

    # 1. Initializes a GlassFlow Python client
    client = glassflow.GlassFlowClient()
    # 2. Creates a pipeline
    pipeline_client = client.pipeline_client(
        pipeline_id=pipeline_id, pipeline_access_token=token
    )

    while True:
        try:
            # 3. Consumes a new event from the pipeline
            response = pipeline_client.consume()

            if response.status_code == 200:
                data = response.body.event
                print("Consumed Data:", data)
        except KeyboardInterrupt:
            print("exiting")
            sys.exit(0)


if __name__ == "__main__":
    load_dotenv()
    main()
