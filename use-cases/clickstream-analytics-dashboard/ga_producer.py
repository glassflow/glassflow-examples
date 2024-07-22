from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    Dimension,
    Metric,
    RunRealtimeReportRequest,
)
from dotenv import load_dotenv
import schedule
import glassflow
import os


class GoogleAnalyticsDataConnector:
    def __init__(self, property_id):
        self.property_id = property_id
        self.client = BetaAnalyticsDataClient()

    def fetch_data(self):
        request = RunRealtimeReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[
                Dimension(name="country"),
                Dimension(name="city"),
                Dimension(name="deviceCategory"),
                Dimension(name="unifiedScreenName"),
            ],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="eventCount"),
                Metric(name="screenPageViews"),
            ],
        )
        response = self.client.run_realtime_report(request)
        return self.process_response(response)

    def process_response(self, response):
        print(f"{response.row_count} rows received")
        data = []
        for row in response.rows:
            record = {}
            for i, dimension_value in enumerate(row.dimension_values):
                dimension_name = response.dimension_headers[i].name
                record[dimension_name] = dimension_value.value
            for i, metric_value in enumerate(row.metric_values):
                metric_name = response.metric_headers[i].name
                record[metric_name] = metric_value.value
            print(data)
            data.append(record)
        return data


def send_message_to_glassflow(data_fetcher, glassflow_client):
    records = data_fetcher.fetch_data()
    for record in records:
        response = glassflow_client.publish(request_body=record)
        if response.status_code == 200:
            print("Message sent to GlassFlow:", record)
        else:
            print(f"Failed to send data to GlassFlow: {response.text}")


def main():
    load_dotenv()

    # Initialize GlassFlow client
    pipeline_id = os.environ["PIPELINE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

    # Initialize Google Analytics data fetcher
    property_id = os.environ["GA_PROPERTY_ID"]
    data_fetcher = GoogleAnalyticsDataConnector(property_id)

    # Schedule message sending to GlassFlow
    EVENTS_PER_SECOND = 5
    schedule.every(float(1 / EVENTS_PER_SECOND)).seconds.do(
        send_message_to_glassflow, data_fetcher, glassflow_client
    )

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
