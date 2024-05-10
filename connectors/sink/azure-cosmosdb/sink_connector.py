import os
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
from azure.cosmos.partition_key import PartitionKey
import time
import random
import glassflow
from dotenv import load_dotenv
import uuid


class SinkConnectorCosmosDB:
    def __init__(self):
        self.cosmosdb_connection_string = os.getenv("AZURE_COSMOSDB_CONNECTION_STRING")
        self.cosmosdb_database_name = os.getenv("AZURE_COSMOS_DB_NAME")
        self.cosmosdb_container_name = os.getenv("AZURE_COSMOS_CONTAINER_NAME")
        self.cosmos_client = None
        self.cosmos_db = None
        self.cosmos_db_container = None

    def setup(self):
        self.cosmos_client = cosmos_client.CosmosClient.from_connection_string(
            self.cosmosdb_connection_string
        )
        self._create_database_if_not_exists()
        self._create_container_if_not_exists()

    def _create_database_if_not_exists(self):
        # Creating database
        try:
            self.cosmos_db = self.cosmos_client.create_database(
                id=self.cosmosdb_database_name
            )
            print("Database with id '{0}' created".format(self.cosmosdb_database_name))
        except errors.CosmosResourceExistsError:
            print(
                "A database with id '{0}' already exists".format(
                    self.cosmosdb_database_name
                )
            )
            self.cosmos_db = self.cosmos_client.get_database_client(
                database=self.cosmosdb_database_name
            )
        except Exception as e:
            print("Error creating database: ", e)

    def _create_container_if_not_exists(self):
        partition_key = PartitionKey(path="/user_id")
        container_name = self.cosmosdb_container_name
        try:
            self.cosmos_db_container = self.cosmos_db.create_container(
                id=container_name, partition_key=partition_key
            )
            print("Container with id '{0}' created".format(container_name))
        except errors.CosmosResourceExistsError:
            print("A container with id '{0}' already exists".format(container_name))
            self.cosmos_db_container = self.cosmos_db.get_container_client(
                container_name
            )
        except Exception as e:
            print("Error creating container: ", e)

    def put(self, data):
        data["id"] = str(uuid.uuid4())
        self.cosmos_db_container.upsert_item(body=data)

    def cleanup(self):
        pass


def main():
    sink_connector = SinkConnectorCosmosDB()
    sink_connector.setup()

    pipeline_id = os.environ["PIPELINE_ID"]
    space_id = os.environ["SPACE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]

    # Create GlassFlow client
    pipeline_client = glassflow.GlassFlowClient().pipeline_client(
        space_id=space_id,
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

    retry_delay = 10
    while True:
        try:
            res = pipeline_client.consume()
            if res.status_code == 204:
                # No new events. sleep for a little bit
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the delay for the next attempt
                retry_delay += random.uniform(0, 1)  # Add jitter
                continue
            if res.status_code == 200:
                record = res.json()
                sink_connector.put(record)
                print("Consumed transformed event from Glassflow and sent to CosmosDB")
                # set the retry delay back to original
                retry_delay = 10
        except KeyboardInterrupt:
            print("Exiting")
            sink_connector.cleanup()
            break


if __name__ == "__main__":
    load_dotenv()
    main()
