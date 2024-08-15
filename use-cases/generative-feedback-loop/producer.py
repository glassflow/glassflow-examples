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


def insert_data(data: List[dict], client: Client, limit: int = None):
    for idx, row in enumerate(data):
        if idx >= limit:
            break

        try:
            if not row['last_review']:
                row['last_review'] = None
            if not row['reviews_per_month']:
                row['reviews_per_month'] = None

            client.table(SUPABASE_TABLE_NAME)\
                .insert(row)\
                .execute()

            print(f"Inserted row {idx+1}")
        except Exception as e:
            if e.code == '23505':
                print(f"Failed to insert data: {e.message}")
            else:
                print(f"Failed to insert data: {row}")
                raise e

        if (idx+1) % 50 == 0:
            time.sleep(1)


if __name__ == '__main__':
    LIMIT = 100
    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    data = load_data()
    insert_data(data, client, limit=LIMIT)
