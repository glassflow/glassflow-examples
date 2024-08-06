import weaviate
import glassflow
import os
import time
import json


class SinkConnectorWeaviate:
    def __init__(self, **kwargs):
        self.http_host = os.getenv("WEAVIATE_HTTP_HOST", "localhost")
        self.http_port = os.getenv("WEAVIATE_HTTP_PORT", 8080)
        self.http_secure = os.getenv("WEAVIATE_HTTP_SECURE", False)
        self.grpc_host = os.getenv("WEAVIATE_GRPC_HOST", "localhost")
        self.grpc_port = os.getenv("WEAVIATE_GRPC_PORT", 50051)
        self.grpc_secure = os.getenv("WEAVIATE_GRPC_SECURE", False)

        self.collection_name = os.getenv("WEAVIATE_COLLECTION")
        self.collection_schema = json.loads(os.getenv("WEAVIATE_COLLECTION_SCHEMA"))

        self.pipeline_id = os.getenv("PIPELINE_ID")
        self.pipeline_access_token = os.getenv("PIPELINE_ACCESS_TOKEN")
        self.pipeline_client = glassflow.GlassFlowClient().pipeline_client(
            pipeline_id=self.pipeline_id,
            pipeline_access_token=self.pipeline_access_token,
        )

        self.weaviate_client = weaviate.connect_to_custom(
            http_host=self.http_host,
            http_port=self.http_port,
            http_secure=self.http_secure,
            grpc_host=self.grpc_host,
            grpc_port=self.grpc_port,
            grpc_secure=self.grpc_secure,
            **kwargs
        )

    def setup(self) -> None:
        self.weaviate_client.connect()

        try:
            while not self.weaviate_client.is_ready():
                time.sleep(0.1)

            if not self._check_collection_exists():
                self._create_collection()
        except Exception as e:
            self.cleanup()
            raise e

    def _check_collection_exists(self) -> bool:
        print(f"Checking if collection {self.collection_name} exists")
        return self.weaviate_client.collections.exists(
            self.collection_name)

    def _create_collection(self) -> None:
        print(f"Creating collection with schema: {self.collection_schema}")
        self.weaviate_client.collections.create_from_dict(
            self.collection_schema)

    def consume(self):
        response = self.pipeline_client.consume()
        return response.json()

    def write(self, data: dict) -> None:
        # The output from the GlassFlow pipeline must have these two fields
        properties = data.get("properties", {})
        vector = data.get("vector", {})

        collection = self.weaviate_client.collections.get(self.collection_name)
        collection.data.insert(properties=properties, vector=vector)

    def cleanup(self):
        self.weaviate_client.close()

    def run(self) -> None:
        self.setup()

        while True:
            try:
                res = self.consume()
                self.write(res)
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                self.cleanup()
                print(f"{self.__name__} connection stopped")


if __name__ == '__main__':
    SinkConnectorWeaviate().run()
