# Clickstream analytics dashboard

This example streaming data pipeline with GlassFlow demonstrates how to build a clickstream analytics dashboard for a typical website using [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1), [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/).

![Clickstream dashboard with GlassFlow](/assets/Clickstream%20analytics%20dashboard%20use%20case.gif)

## Prerequisites

To start with this setup, you need a free GlassFlow account.

- [Sign up for a free account](http://app.glassflow.dev/)
- [Python is installed](https://www.python.org/downloads/) on your machine.
- [Download and install Pip](https://pip.pypa.io/en/stable/installation/) to manage project packages

## Installation

- Use Python script `fake_producer.py` with the Faker library to generate mock clickstream data and push it to GlassFlow. You do not need to Set Up Google Analytics 4 API in this case.
- Use the Google Analytics 4 Data API integration example code in `ga_producer.py` Python script to push real-time report events to GlassFlow. Learn to how [set up Google Analytics API](#steps-to-set-up-google-analytics-4-api).

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd use-cases/clickstream-analytics-dashboard
    ```

3. Create a new virtual environment:
    
    ```bash
    python -m venv .venv && source .venv/bin/activate
    ```
    
4. Install the required dependencies:
    
    ```
    pip install -r requirements.txt
    ```    

## Steps to run the GlassFlow pipeline

### 1. Setting Up the Pipeline with GlassFlow WebApp

Follow the [easy steps in the tutorial](https://docs.glassflow.dev/tutorials/use-cases/real-time-clickstream-analytics#setting-up-the-pipeline-with-glassflow) to create a pipeline using GlassFlow WebApp.

### 2. Create an environment configuration file

Add a `.env` file in the project directory and add the following configuration variables:

```bash
PIPELINE_ID=your_pipeline_id
PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
```

Replace `your_pipeline_id` and `your_pipeline_access_token` with appropriate values obtained from your GlassFlow account.

## Steps to set up Google Analytics 4 API

### 1. Enable Google Analytics Data APIs 

[Enable the Google Analytics Data API](https://console.cloud.google.com/flows/enableapi?apiid=analyticsdata.googleapis.com)
and create a [new project](https://console.cloud.google.com/projectcreate) or select an existing project.

### 2. Create a Service Account

Go to https://console.cloud.google.com/apis/credentials. Click "Create credentials" and choose a "Service Account" option. Name the service user and click through the next steps.

### 3. Create a new credential for the service account

Once more go to https://console.cloud.google.com/apis/credentials and click on your newly created user (under Service Accounts)
Go to "Keys", click "Add key" -> "Create new key" -> "JSON". A JSON file will be saved to your computer.

### 4. Set the path to the JSON file

Rename this JSON file to credentials.json and put it under `use-cases/clickstream-analytics-dashboard`. Then set the path to
this file to the environment variable `GOOGLE_APPLICATION_CREDENTIALS`:

```sh
export GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### 5. Add the service account to the Google Analytics property

Use the service account email address to [add a user](https://support.google.com/analytics/answer/1009702) to the Google Analytics [property](https://developers.google.com/analytics/devguides/reporting/data/v1/property-id) you want to access via the Google Analytics Data API v1. For this tutorial, only [Viewer](https://support.google.com/analytics/answer/9305587) permissions are needed.

### 6. Copy the Google Analytics property ID

Copy the Google Analytics [property ID](https://developers.google.com/analytics/devguides/reporting/data/v1/property-id) you are discovering and save it to variable value for `GA_PROPERTY_ID` in the `.env` file in the project directory.

## Run the pipeline

### 1. Run data producer

Run the `fake_producer.py` or `ga_producer.py` script to start publishing data:

```bash
python fake_producer.py
```

### 2. Run the dashboard

Run the `consumer.py` with Streamlit command to run the dashboard:

```bash
streamlit run consumer.py
```
