

import streamlit as st
import time
import sys
import os
from weaviate.classes.query import Filter

from typing import Optional, List

import pandas as pd
import weaviate
from streamlit.connections import BaseConnection
from weaviate.client import WeaviateClient
from weaviate.auth import _APIKey
from weaviate.classes.init import Auth
from weaviate.collections.classes.data import DataObject
from weaviate.collections.classes.types import WeaviateProperties


def weaviate_response_objects_to_df(
    objects: List[DataObject[WeaviateProperties, None]]
) -> pd.DataFrame:
    """
    Convert a list of Weaviate DataObjects to a pandas DataFrame.
    """
    if objects:
        df = pd.json_normalize([obj.properties for obj in objects])
        return df
    else:
        return None


class WeaviateConnection(BaseConnection["WeaviateClient"]):
    """
    A Streamlit connection to a Weaviate database.
    """

    def __init__(
        self,
        connection_name: str,
        http_host: str = 'localhost',
        http_port: int = 8080,
        http_secure: bool = False,
        grpc_host: str = 'localhost',
        grpc_port: int = 50051,
        grpc_secure: bool = False,
        api_key=None,
        additional_headers=None,
        **kwargs,
    ) -> None:

        self.http_host = http_host
        self.http_port = http_port
        self.http_secure = http_secure
        self.grpc_host = grpc_host
        self.grpc_port = grpc_port
        self.grpc_secure = grpc_secure

        self.api_key = api_key
        self.additional_headers = additional_headers
        self._client = weaviate.connect_to_custom(
            http_host=self.http_host,
            http_port=self.http_port,
            http_secure=self.http_secure,
            grpc_host=self.grpc_host,
            grpc_port=self.grpc_port,
            grpc_secure=self.grpc_secure,
            auth_credentials=self._create_auth_config(),
            headers=self.additional_headers,
            skip_init_checks=True,
        )
        super().__init__(connection_name, **kwargs)

    def _connect(self) -> WeaviateClient:
        self._client.connect()
        return self._client

    def _create_auth_config(self) -> Optional[_APIKey]:
        api_key = self.api_key or self._secrets.get("WEAVIATE_API_KEY")
        if api_key is not None:
            return Auth.api_key(api_key=api_key)
        else:
            return None

    def client(self) -> WeaviateClient:
        """
        Connect to Weaviate and return the client object for use in queries.
        """

        self._connect()

        return self._client

    def close(self) -> None:
        """
        Close the connection to Weaviate.
        """

        self._client.close()

        return None


# Constants
ENV_VARS = ["OPENAI_API_KEY", "WEAVIATE_HTTP_HOST", "WEAVIATE_HTTP_PORT",
            "WEAVIATE_HTTP_SECURE", "WEAVIATE_GRPC_HOST", "WEAVIATE_GRPC_PORT",
            "WEAVIATE_GRPC_SECURE"]
SEARCH_LIMIT = 5


# Functions
def get_env_vars(env_vars):
    """Retrieve environment variables"""
    env_vars = {var: os.environ.get(var, "") for var in env_vars}
    for var, value in env_vars.items():
        if not value:
            st.error(f"{var} not set", icon="🚨")
            sys.exit(f"{var} not set")
    return env_vars


def clean_input(input_text):
    """Clean user input"""
    return input_text.replace('"', "").replace("'", "")


def setup_sidebar():
    """Setup sidebar elements"""
    with st.sidebar:
        st.title("AirBnB search")
        st.subheader("The RAG Recommender")
        st.markdown("Your GlassFlow & Weaviate & AI powered apartment recommender. "
                    "Find the perfect apartment for your holidays. Just tell us what you're looking for!")
        st.header("Filters")

        price_range = st.slider("Price range", min_value=0, max_value=1000, value=(0, 1000))
        st.success("Connected to Weaviate", icon="💚")

    return price_range


def setup_weaviate_connection(env_vars: dict):
    """Setup Weaviate connection"""
    return st.connection(
        "weaviate",
        type=WeaviateConnection,
        http_host=env_vars["WEAVIATE_HTTP_HOST"],
        http_port=env_vars["WEAVIATE_HTTP_PORT"],
        http_secure=env_vars["WEAVIATE_HTTP_SECURE"],
        grpc_host=env_vars["WEAVIATE_GRPC_HOST"],
        grpc_port=env_vars["WEAVIATE_GRPC_PORT"],
        grpc_secure=env_vars["WEAVIATE_GRPC_SECURE"],
        additional_headers={"X-OpenAI-Api-Key": env_vars["OPENAI_API_KEY"]},
    )


def perform_search(conn, query, rag_prompt, price_range):
    """Perform search and display results"""
    with conn.client() as client:
        collection = client.collections.get("Listing")
        listings = collection.query.near_text(
            query=query,
            return_properties=["name", "price", "neighbourhood", "summary"],
            filters=(
                Filter.by_property("price").greater_or_equal(price_range[0]) &
                Filter.by_property("price").less_or_equal(price_range[1])
            ),
            limit=SEARCH_LIMIT,
        )
        df = weaviate_response_objects_to_df(listings.objects)

    if df is None or df.empty:
        with st.chat_message("assistant"):
            st.write(f"No accommodations found matching your price range. Please try again.")
        st.session_state.messages.append({"role": "assistant", "content": "No movies found. Please try again."})
        return
    else:
        with st.chat_message("assistant"):
            st.write("Raw search results.")
            st.dataframe(data=df)
            st.write("Now generating recommendation from these: ...")

        with conn.client() as client:
            collection = client.collections.get("Listing")
            response = collection.generate.hybrid(
                query=rag_prompt,
                filters=(
                    Filter.by_property("price").greater_or_equal(price_range[0]) &
                    Filter.by_property("price").less_or_equal(price_range[1])
                ),
                limit=SEARCH_LIMIT,
                alpha=1,
                grouped_task=rag_prompt,
                grouped_properties=["name", "summary"],
            )

            rag_response = response.generated

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in rag_response.split():
                    full_response += chunk + " "
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": "Recommendation from these search results: " + full_response}
        )


def main():
    st.title("Search for apartments")

    env_vars = get_env_vars(ENV_VARS)
    conn = setup_weaviate_connection(env_vars)
    price_range = setup_sidebar()

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.greetings = False

    if not st.session_state.greetings:
        with st.chat_message("assistant"):
            intro = ("👋 Welcome to Airbnb Magic! I'm your AI apartment recommender. "
                     "Tell me what kind of place you're in the mood for and the occasion, "
                     "and I'll suggest some great options.")
            st.markdown(intro)
            st.session_state.messages.append({"role": "assistant", "content": intro})
            st.session_state.greetings = True

    if "example_movie_type" not in st.session_state:
        st.session_state.example_movie_type = ""
    if "example_occasion" not in st.session_state:
        st.session_state.example_occasion = ""

    query = clean_input(st.text_input(
        "What are you looking for in your accommodation?",
        value=st.session_state.example_occasion,
        placeholder="E.g., spacious, centric"
    ))

    if st.button("Search") and query:
        rag_prompt = (f"Suggest one to two accommodations out of the following "
                      f"list, taking into account the user's request: {query}. "
                      f"Give a concise yet fun and positive recommendation.")
        prompt = f"Searching for: {query}"
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        perform_search(conn, query, rag_prompt, price_range)
        # st.rerun()


if __name__ == "__main__":
    main()
