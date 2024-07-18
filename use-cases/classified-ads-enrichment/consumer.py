from dotenv import load_dotenv
import glassflow
import os
import redis
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import TextField, TagField
from redis.commands.json.path import Path
import sys

load_dotenv()

PIPELINE_ID = os.environ.get("PIPELINE_ID")
PIPELINE_ACCESS_TOKEN = os.environ.get("PIPELINE_ACCESS_TOKEN")

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = os.getenv('REDIS_DB', 0)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


def write_document(client: redis.Redis, document: dict):
    print("Writing document...")
    client.json().set(
        f"classified:{document['id']}",
        Path.root_path(),
        document)
    print("Document written.")


def create_classifieds_index(client: redis.Redis) -> None:
    indices = client.execute_command('FT._LIST')
    if b"idx:classified" not in indices:
        print("Creating classifieds index...")

        schema = (
            TextField("$.id", as_name="id"),
            TextField("$.user_id", as_name="user_id"),
            TextField("$.title", as_name="title"),
            TextField("$.description", as_name="description"),
            TagField("$.category", as_name="category"),
            TextField("$.summary", as_name="summary"),
        )

        rs = client.ft("idx:classified")
        rs.create_index(
            schema,
            definition=IndexDefinition(
                prefix=["classified:"],
                index_type=IndexType.JSON
            )
        )
        print("Created classifieds index.")


def main():
    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(
        pipeline_id=PIPELINE_ID,
        pipeline_access_token=PIPELINE_ACCESS_TOKEN
    )

    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD)

    # Create index if it does not exist
    create_classifieds_index(redis_client)

    while True:
        try:
            res = pipeline_client.consume()
            if res.status_code == 200:
                write_document(redis_client, res.body.event)
        except KeyboardInterrupt:
            print("exiting")
            sys.exit(0)


if __name__ == "__main__":
    main()
