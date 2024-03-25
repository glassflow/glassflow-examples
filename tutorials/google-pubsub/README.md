# GlassFlow and Google Pub/Sub Integration Pipeline Example

This repository demonstrates how to integrate Google Cloud Pub/Sub with GlassFlow to ingest and transform real-time data.

![GlassFlow Google Pubsub](/assets/GlassFlow%20Google%20Pubsub.png)

## Prerequisites

To run the sample pipeline you'll need the following:

- [Python is installed](https://www.python.org/downloads/) on your machine.
- [Pip](https://pip.pypa.io/en/stable/installation/) is installed to manage project packages.
- You created a [GlassFlow account](https://www.notion.so/o/aR82XtsD8fLEkzPmMtb7/s/pRyi93X0Jn9wrh2Z4Ffm/~/changes/9/get-started/create-account).
- You installed [GlassFlow CLI](https://www.notion.so/o/aR82XtsD8fLEkzPmMtb7/s/pRyi93X0Jn9wrh2Z4Ffm/~/changes/9/get-started/glassflow-cli) and logged into your account via the CLI.
- Follow [steps from 1 to 7](https://cloud.google.com/pubsub/docs/publish-receive-messages-client-library) under Before you begin section of guidance on [Google Pub/Sub get started documentation](https://cloud.google.com/pubsub/docs/publish-receive-messages-client-library) to install the Google Cloud CLI and create a new Google Cloud project called `glassflow-data-pipeline`.

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd tutorials/google-pubsub
    ```
3. Create a new virtual environment
Create a new virtual environment in the same folder and activate that environment:
    
    ```bash
    virtualenv glassflow && source glassflow/bin/activate
    ```

3. Install the GlassFlow, Google Cloud PubSub Python SDKs and virtual environment package python-dotenvusing pip.

    ```bash
    pip install glassflow python-dotenv google-cloud-pubsub
    ```

4. Read the following tutorial to learn how run the project: [Integrating Google Pub/Sub with GlassFlow](https://learn.glassflow.dev/docs/develop/tutorials/integrating-google-pub-sub-with-glassflow)https://learn.glassflow.dev/docs/develop/tutorials/integrating-google-pub-sub-with-glassflow.
