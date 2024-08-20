from typing import List, Dict
from openai import OpenAI
import os
import uuid

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_CHAT_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Name of the Weaviate Collection the output will be stored into
WEAVIATE_CLASS_NAME = "Listing"


def get_embedding(text: str, client: OpenAI) -> List[float]:
    text = text.replace("\n", " ")
    return client.embeddings.create(
        input=[text],
        model=OPENAI_EMBEDDING_MODEL
    ).data[0].embedding


def get_summary(data: Dict[str, str], client: OpenAI) -> str:
    generatePrompt = f"""
    Please write a description for the following AirBnB Listing in English. 
    NAME: {data['name']} 
    HOST_NAME {data['host_name']} 
    NEIGHBOURHOOD {data['neighbourhood']}
    NEIGHBOURHOOD_GROUP {data['neighbourhood_group']} 
    PRICE {data['price']}.
    
    Please do not make up any information about the property in your description."""

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": generatePrompt
            }
        ],
        model=OPENAI_CHAT_MODEL
    )

    return response.choices[0].message.content


def handler(data, logs):
    client = OpenAI()

    try:
        logs.info("Generating summary and vector embeddings...")
        summary = get_summary(data["record"], client)
        vector = get_embedding(summary, client)
        logs.debug(f"Summary generated: {summary}")
    except Exception as e:
        logs.error("Failed to generate summary and vector embeddings.", e)
        raise e

    properties = data["record"]
    listing_id = properties.pop("id")
    properties["summary"] = summary

    return {
        "class": WEAVIATE_CLASS_NAME,
        "id": str(uuid.UUID(int=listing_id)),
        "properties": properties,
        "vector": vector
    }
