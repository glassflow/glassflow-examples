from dotenv import load_dotenv
import schedule
from faker import Faker
import glassflow
import os
import random


class DataGenerator:
    def __init__(self):
        # Define a list of actions/events
        self.actions = [
            "logged in",
            "accessed file",
            "executed command",
            "accessed directory",
        ]
        self.fake = Faker()

    def generate_record(self):
        log = ""
        timestamp = self.fake.date_time_this_year().strftime("[%d/%b/%Y %H:%M:%S]")
        ip_address = self.fake.ipv4()
        user = self.fake.user_name()
        action = random.choice(self.actions)
        if action == "logged in":
            log = f"{timestamp} {ip_address} {user} {action} successfully"
        elif action == "accessed file":
            file_name = self.fake.file_name()
            log = f"{timestamp} {ip_address} {user} {action} '{file_name}'"
        elif action == "executed command":
            command = self.fake.word()
            log = f"{timestamp} {ip_address} {user} executed command '{command}'"
        elif action == "accessed directory":
            directory = self.fake.file_path(depth=random.randint(1, 3))
            log = f"{timestamp} {ip_address} {user} accessed directory '{directory}'"
        return log


def send_message_to_glassflow(record_function, glassflow_client):
    record = record_function()
    response = glassflow_client.publish(request_body=record)
    if response.status_code == 200:
        print("Message sent to GlassFlow:", record)
    else:
        print(f"Failed to send data to GlassFlow: {response.text}")


def main():
    # Initialize GlassFlow client
    pipeline_id = os.environ["PIPELINE_ID"]
    space_id = os.environ["SPACE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        space_id=space_id,
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

    # Initialize data generator
    data_generator = DataGenerator()

    # Schedule message sending to GlassFlow
    EVENTS_PER_SECOND = 5
    schedule.every(float(1 / EVENTS_PER_SECOND)).seconds.do(
        send_message_to_glassflow, data_generator.generate_record, glassflow_client
    )

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    load_dotenv()
    main()
