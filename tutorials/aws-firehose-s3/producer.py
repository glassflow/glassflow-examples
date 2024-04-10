import random
from faker import Faker
from dotenv import dotenv_values
from glassflow import GlassFlowClient

config = dotenv_values(".env")

pipeline_id = config.get("PIPELINE_ID")
space_id = config.get("SPACE_ID")
token = config.get("PIPELINE_ACCESS_TOKEN")


class RecordGenerator:
    def __init__(self):
        self.userid = 0
        self.channelid = 0
        self.genre = ""
        self.lastactive = None
        self.title = ""
        self.watchfrequency = 0
        self.etags = None

    def generate_netflix_record(self, fake):
        netflix_data = {
            "userid": fake.uuid4(),
            "channelid": fake.pyint(min_value=1, max_value=50),
            "genre": random.choice(["thriller", "comedy", "romcom", "fiction"]),
            "lastactive": fake.date_time_between(
                start_date="-10m", end_date="now"
            ).isoformat(),
            "title": fake.name(),
            "watchfrequency": fake.pyint(min_value=1, max_value=10),
            "etags": fake.uuid4(),
        }
        return netflix_data


def main():
    try:
        glassflow_client = GlassFlowClient().pipeline_client(
            space_id=space_id, pipeline_id=pipeline_id, pipeline_access_token=token
        )
        fake = Faker()
        max_records = 5

        generator = RecordGenerator()

        # Generate and stream data
        while True and max_records > 0:
            data_json = generator.generate_netflix_record(fake)
            max_records -= 1
            try:
                print(f"Sending record to GlassFlow pipeline: '{data_json}'")
                glassflow_client.publish(request_body=data_json)
            except Exception as e:
                print(f"Failed to push data to GlassFlow: {e}")
    except Exception as e:
        print("Error:", e)
        raise


if __name__ == "__main__":
    main()
