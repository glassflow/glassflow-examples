# Real-time data anomaly detection with AI

This example real-time pipeline demonstrates data anomaly detection with GlassFlow and OpenAI to monitor server logs to detect unusual patterns or suspicious activities and send notifications to Slack.


## Prerequisites

Make sure that you have the following before proceeding with the installation:

- [Sign up for a free GlassFlow account](http://app.glassflow.dev/).
- You have [OpenAI API](https://openai.com/api/) account.
- Slack account: If don't have a Slack account, sign up for a new free one [here](https://slack.com/get-started) and go to the Slack [Get Started page](https://slack.com/get-started#/createnew).
- Slack workspace: You need access to a Slack workspace where you're an admin. If you are creating just a new workspace, follow [this guide](https://slack.com/help/articles/206845317-Create-a-Slack-workspace).
- You created an [incoming webhook](https://api.slack.com/messaging/webhooks) for your Slack workspace.

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd use-cases/real-time-data-anomaly-detection
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

Follow the [easy steps in the tutorial](https://docs.glassflow.dev/tutorials/use-cases/real-time-log-data-anomaly-detection) to create a pipeline using GlassFlow WebApp.

### 2. Create an environment configuration file

Add a `.env` file in the project directory and add the following configuration variables:

```bash
PIPELINE_ID=your_pipeline_id
PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
```

Replace `your_pipeline_id` and `your_pipeline_access_token` with appropriate values obtained from your GlassFlow account.

## Send sample log data to the pipeline

### Run the log producer
Run `producer.py` Python script in a terminal to publish sample server log data to the GlassFlow pipeline:

```bash
python producer.py
```

This script will continuously consume new events from the GlassFlow pipeline. Upon receiving transformed events, it will send notifications to Slack. You should see an output indicating that messages are being received on Slack.