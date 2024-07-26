import os
import uuid
import time
import random
import redis
from redis.commands.json.path import Path
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import TextField
import glassflow
from dotenv import load_dotenv


class SinkConnectorRedis:
    def __init__(self):
        load_dotenv()
        self.redis_host = os.getenv("REDIS_HOST")
        self.redis_password = os.getenv("REDIS_PASSWORD", None)
        self.redis_port = os.getenv("REDIS_PORT", 6379)
        self.redis_db = os.getenv("REDIS_DB", "0")
        self.redis_index = os.getenv("REDIS_INDEX", "idx")

        self.pipeline_id = os.getenv("PIPELINE_ID")
        self.pipeline_access_token = os.getenv("PIPELINE_ACCESS_TOKEN")
        self.pipeline_client = glassflow.GlassFlowClient().pipeline_client(
            pipeline_id=self.pipeline_id,
            pipeline_access_token=self.pipeline_access_token,
        )

        self.redis_client = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db,
            password=self.redis_password
        )

    def setup(self):
        if not self._index_exists():
            print("Creating Redis index:", self.redis_index)
            self._create_index()
            time.sleep(30)  # Wait for index to be created
        else:
            print("Redis index already exists:", self.redis_index)

    def _index_exists(self):
        """
        Check if Redis index exists
        """
        indices = self.redis_client.execute_command('FT._LIST')
        print("Existing Redis indices:", indices)
        indices = [idx.decode() for idx in indices]
        return self.redis_index in indices

    def _create_index(self):
        """
        Create Redis index
        """
        try:
            schema = (
                TextField("$.id", as_name="id")
            )

            rs = self.redis_client.ft(self.redis_index)
            rs.create_index(
                schema,
                definition=IndexDefinition(
                    index_type=IndexType.JSON
                )
            )
            print("Redis index created successfully:", self.redis_index)
        except Exception as e:
            print("Failed to create Redis index:", e)
            raise e

    def set(self, data):
        try:
            record_id = str(uuid.uuid4())
            self.redis_client.json().set(
                record_id,
                Path.root_path(),
                data)
            print("Record written to Redis:", data)
        except Exception as e:
            print("Failed to set record to Redis:", e)

    def cleanup(self):
        pass


def main():
    sink_connector = SinkConnectorRedis()
    sink_connector.setup()

    pipeline_id = os.environ["PIPELINE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]

    # Create GlassFlow client
    pipeline_client = glassflow.GlassFlowClient().pipeline_client(
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
                sink_connector.set(record)
                print("Consumed transformed event from Glassflow and sent to Redis")
                # set the retry delay back to original
                retry_delay = 10
        except KeyboardInterrupt:
            print("Exiting")
            sink_connector.cleanup()
            break


if __name__ == "__main__":
    load_dotenv()
    main()
