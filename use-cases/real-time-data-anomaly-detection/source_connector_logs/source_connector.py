import os
import schedule
import time
from dotenv import load_dotenv
from data_generator import DataGenerator
import glassflow

class SourceConnectorLogs:
    def __init__(self):
        load_dotenv()
        self.pipeline_id = os.getenv("PIPELINE_ID")
        self.pipeline_access_token = os.getenv("PIPELINE_ACCESS_TOKEN")
        self.data_generator = DataGenerator()
        self.glassflow_client = glassflow.GlassFlowClient().pipeline_client(
            pipeline_id=self.pipeline_id,
            pipeline_access_token=self.pipeline_access_token,
        )

    def setup(self):
        pass

    def send_log_to_glassflow(self):
        log_data = self.data_generator.generate_log()
        response = self.glassflow_client.publish(request_body=log_data)
        if response.status_code == 200:
            print("Log sent to GlassFlow:", log_data)
        else:
            print(f"Failed to send log to GlassFlow: {response.text}")

    def run(self):
        EVENTS_PER_SECOND = 5
        schedule.every(float(1 / EVENTS_PER_SECOND)).seconds.do(self.send_log_to_glassflow)

        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                print("Exiting...")
                break

def main():
    source_connector = SourceConnectorLogs()
    source_connector.setup()
    source_connector.run()

if __name__ == "__main__":
    main()
