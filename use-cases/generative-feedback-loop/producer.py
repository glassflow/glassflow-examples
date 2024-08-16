import sys
import os
import time
from csv import DictReader
from typing import List
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
SUPABASE_TABLE_NAME: str = 'Airbnb-nyc-2019'
DATASET_PATH: str = "data/AB_NYC_2019.csv"


def load_data() -> List[dict]:
    with open(DATASET_PATH, "r") as f:
        reader = DictReader(f)
        return list(reader)


def update_table(data: List[dict], client: Client, limit: int = None):
    for idx, row in enumerate(data):
        if idx >= limit:
            break

        try:
            client.table(SUPABASE_TABLE_NAME)\
                .update({"is_listing_in_weaviate": True})\
                .eq("id", row["id"])\
                .execute()
            print(f"Updated row {idx + 1}")
        except Exception as e:
            print(f"Failed to insert data: {row}")
            raise e
        if (idx+1) % 50 == 0:
            time.sleep(1)


if __name__ == '__main__':
    LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    data = load_data()
    update_table(data, client, limit=LIMIT)
