from vertexai.preview.language_models import TextEmbeddingModel, TextEmbeddingInput
from google.cloud import aiplatform
from google.oauth2 import service_account
import json
import os


def handler(data, log):
    model_id = os.getenv("MODEL_ID", "text-embedding-004")
    project_id = os.getenv("GCP_PROJECT_ID")
    region = os.getenv("GCP_REGION", "us-central1")
    credential_json = os.getenv("GCP_SERVICE_ACCOUNT_JSON")

    try:
        json_account_info = json.loads(credential_json, strict=False)
        credentials = service_account.Credentials.from_service_account_info(json_account_info)

        aiplatform.init(
            project=project_id,
            location=region,
            credentials=credentials,
        )

        model = TextEmbeddingModel.from_pretrained(model_id)
        text_embedding_input = TextEmbeddingInput(
            task_type="RETRIEVAL_QUERY",
            text=data["content"]
        )
        embeddings = model.get_embeddings([text_embedding_input])[0]
        vector_id = data.pop("id")

        # Format output to match expected JSON from Pinecone connector
        upsert_json = {
            "operation": "upsert",
            "data": {
                "namespace": "ns",
                "vectors": [
                    {
                        "id": vector_id,
                        "values": embeddings.values,
                        "metadata": data,
                    },
                ],
            },
        }
    except Exception as e:
        log.error(e)
        raise e

    log.info(f"Upsert Event: {upsert_json}")
    return upsert_json
