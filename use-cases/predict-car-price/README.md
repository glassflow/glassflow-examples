# Real-time car price data recommendation pipeline using AI

This example streaming data pipeline with GlassFlow demonstrates how to monitor real-time car data events
and predict future prices using OpenAI.

## Prerequisites

Make sure that you have the following before proceeding with the installation:

- [Sign up for a free GlassFlow account](http://app.glassflow.dev/).
- You have [OpenAI API](https://openai.com/api/) account.

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd use-cases/predict-car-price
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

Follow the [easy steps in the tutorial](https://docs.glassflow.dev/tutorials/use-cases/real-time-price-recommendation#setting-up-the-pipeline-with-glassflow) to create a pipeline using GlassFlow WebApp.

### 2. Create an environment configuration file

Add a `.env` file in the project directory and add the following configuration variables:

```bash
PIPELINE_ID=your_pipeline_id
PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
```

Replace `your_pipeline_id` and `your_pipeline_access_token` with appropriate values obtained from your GlassFlow account.

## Run the pipeline
You'll run the producer and consumer Python scripts to test the pipeline.

### Run data producer

Run the `producer.py` script to start publishing data:

```bash
python producer.py
```

### Run data consumer

Run the `consumer.py` to retrieve transformed data from the pipeline:

```bash
python consumer.py
```
