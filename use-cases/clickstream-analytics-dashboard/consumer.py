import glassflow
import sys
from dotenv import load_dotenv
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import time

load_dotenv()

pipeline_id = os.environ["PIPELINE_ID"]
token = os.environ["PIPELINE_ACCESS_TOKEN"]
client = glassflow.GlassFlowClient()
pipeline_client = client.pipeline_client(
    pipeline_id=pipeline_id, pipeline_access_token=token
)

st.title("Clickstream Analytics Dashboard")

placeholder = st.empty()


def update_dashboard(data):
    if data:
        df = pd.DataFrame(data)

        # User Engagement by Web Page and Location
        fig_engagement = px.bar(
            df,
            x="unifiedScreenName",
            y="engagement_score",
            color="city",
            title="User Engagement by Web Page and Location",
        )

        # Device Usage
        device_usage_df = (
            pd.json_normalize(df["device_usage"].tolist()).sum().reset_index()
        )
        device_usage_df.columns = ["Device", "Count"]
        fig_device = px.pie(
            device_usage_df,
            names="Device",
            values="Count",
            title="Device Usage Distribution",
        )

        # Content Popularity
        content_popularity_list = []
        for cp in df["content_popularity"]:
            for page, metrics in cp.items():
                content_popularity_list.append(
                    {
                        "page": page,
                        "event_count": metrics["event_count"],
                        "screen_page_views": metrics["screen_page_views"],
                    }
                )
        content_popularity_df = pd.DataFrame(content_popularity_list)
        fig_content = px.bar(
            content_popularity_df,
            x="page",
            y="event_count",
            title="Content Popularity (Event Count)",
        )

        # Geographic Distribution
        geographic_distribution_list = []
        for geo in df["geographic_distribution"]:
            for country, metrics in geo.items():
                geographic_distribution_list.append(
                    {
                        "country": country,
                        "city": metrics["city"],
                        "active_users": metrics["active_users"],
                    }
                )
        geo_dist_df = pd.DataFrame(geographic_distribution_list)
        fig_geo = px.bar(
            geo_dist_df,
            x="country",
            y="active_users",
            color="city",
            title="Geographic Distribution of Active Users",
        )

        # Display the figures in a 2x2 grid
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_engagement)
            st.plotly_chart(fig_device)
        with col2:
            st.plotly_chart(fig_content)
            st.plotly_chart(fig_geo)


data = []

while True:
    with placeholder.container():
        try:
            # consume transformed data from the pipeline
            res = pipeline_client.consume()
            if res.status_code == 200:
                # get the transformed data as json
                event_data = res.body.event
                print("Data consumed successfully")
                print(event_data)

                data.append(event_data)
                print(data)

                # update the dashboard
                update_dashboard(data)
        except KeyboardInterrupt:
            print("exiting")
            sys.exit(0)
        time.sleep(2)
