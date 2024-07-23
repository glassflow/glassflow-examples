# Real-time data anomaly detection with AI

This example real-time pipeline demonstrates data anomaly detection with GlassFlow and OpenAI to monitor server logs to detect unusual patterns or suspicious activities and send notifications to Slack.

Follow these steps to run the pipeline.

## Prerequisites

Make sure that you have the following before proceeding with the installation:

- [Docker](https://www.docker.com/get-started) is installed on your machine
- You created a [GlassFlow account](https://docs.glassflow.dev/get-started/create-account).
- You installed [GlassFlow CLI](https://docs.glassflow.dev/get-started/glassflow-cli#installation) and logged into your account via the CLI.
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

### Steps to run GlassFlow pipeline

#### 1. Get a new OpenAI API Key

 Create [API key](https://platform.openai.com/api-keys) to use [OpenAI API](https://platform.openai.com/docs/api-reference/authentication) endpoints.

#### 2. Set OpenAI API Key

Open `transform.py` file and replace `{REPLACE_WITH_YOUR_OPENAI_API_KEY}` with your actual API key.

#### 3. Create a Space via CLI

Open a terminal and create a new space called `examples` to organize multiple pipelines:

```bash
glassflow space create examples
```

After the space is created successfully, you will get a SpaceID in the terminal.

#### 4. Create a Pipeline via CLI

Use the GlassFlow CLI to create a new data pipeline inside the space. 

```bash
glassflow pipeline create anomalies-detection --space-id={space_id} --function=transform.py --requirements=openai
```

This command initializes the pipeline with a name `anomalies-detection` in the `examples` space and specifies the transformation function `transform.py`. After running the command, it returns a new **Pipeline ID** with its **Access Token**.

#### 5. Create an environment configuration file

Add a `.env` file in the project directory and add the following configuration variables:

```bash
SLACK_WEBHOOK_URL=your_slack_workspace_webhook_url
PIPELINE_ID=your_pipeline_id
PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
```

Replace `your_pipeline_id`, `your_pipeline_access_token` and `your_slack_workspace_webhook_url` with appropriate values obtained from your GlassFlow pipeline and Slack Workspace.

#### 6. Run the project with Docker Compose:
    
    ```bash
    docker compose up
    ```
