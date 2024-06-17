# Clickstream analytics dashboard

This example streaming data pipeline with GlassFlow demonstrates how to build a clickstream analytics dashboard using [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1), [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/).

![Clickstream dashboard with GlassFlow](/assets/Clickstream%20analytics%20dashboard%20use%20case.gif)

Follow these steps to run the pipeline.

## Prerequisites

Make sure that you have the following before proceeding with the installation:

- You created a [GlassFlow account](https://learn.glassflow.dev/docs/get-started/create-account).
- You installed [GlassFlow CLI](https://learn.glassflow.dev/docs/get-started/glassflow-cli) and logged into your account via the CLI.
- Basic knowledge of Google Analytics, Streamlit, and Plotly.

## Installation

We'll use the [GlassFlow CLI](https://learn.glassflow.dev/docs/get-started/glassflow-cli) to create a new space and configure the data pipeline. There are two options for data producers:

- Use Python script `fake_producer.py` with the Faker library to generate mock clickstream data and push it to GlassFlow. You do not need to Set Up Google Analytics 4 API in this case.
- Use the Google Analytics 4 Data API integration example code in `ga_producer.py` Python script to push real-time report events to GlassFlow. Learn to how set up Google Analytics 4 API in the tutorial.

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

### Steps to run the GlassFlow pipeline

#### 1. Create a Space via CLI

Open a terminal and create a new space called `examples` to organize multiple pipelines:

```bash
glassflow space create examples
```

After creating the space successfully, you will get a `SpaceID` in the terminal.

#### 2. Create a Pipeline via CLI

Create a new data pipeline inside the space.

```bash
glassflow pipeline create clickstream-analytics-dashboard --space-id={space_id} --function=transform.py
```

This command initializes the pipeline with the name `clickstream-analytics-dashboard` in the `examples` space and specifies the transformation function `transform.py`. After running the command, it returns a new **Pipeline ID** with its **Access Token**.

#### 3. Create an environment configuration file

Add a `.env` file in the project directory and add the following configuration variables:

```bash
GA_PROPERTY_ID=your_ga_property_id # You do not need it if you generate mock events using fake_producer.py.
PIPELINE_ID=your_pipeline_id
SPACE_ID=your_space_id
PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
```

Replace `your_pipeline_id`, `your_space_id`, and `your_pipeline_access_token` with appropriate values obtained from your GlassFlow account.

#### 4. Run data producer

Run the `fake_producer.py` script to start publishing data:

```bash
python fake_producer.py
```

#### 5. Run the dashboard

Run the `dashboard.py` with Streamlit command to run the dashboard:

```bash
streamlit run dashboard.py
```
