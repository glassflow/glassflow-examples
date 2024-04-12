# Integrating AWS Kinesis Data Firehose with GlassFlow

This tutorial demonstrates how to build an end-to-end serverless streaming data pipeline with GlassFlow, AWS Kinesis and AWS S3.

## Prerequisites

To run the sample pipeline you'll need the following:

- [Python is installed](https://www.python.org/downloads/) on your machine.
- [Pip](https://pip.pypa.io/en/stable/installation/) is installed to manage project packages.
- You created a [GlassFlow account](https://learn.glassflow.dev/docs/get-started/create-account#create-a-new-account), installed [GlassFlow CLI](https://learn.glassflow.dev/docs/get-started/glassflow-cli#installation), and logged into your account via the CLI.
- You have an [AWS account](https://portal.aws.amazon.com/).
- You installed [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd tutorials/aws-firehose-s3
    ```
3. Create a new virtual environment in the same folder and activate that environment:
    
    ```bash
    python -m venv .venv && source .venv/bin/activate
    ```

4. Install the GlassFlow, AWS Boto3 Python SDKs, and virtual environment package python-dotenvusing pip.

    ```bash
    pip install glassflow python-dotenv boto3 faker
    ```

5. Read the following tutorial to learn how to run the project: [Integrating AWS Kinesis Data Firehose with GlassFlow](https://app.gitbook.com/o/aR82XtsD8fLEkzPmMtb7/s/pRyi93X0Jn9wrh2Z4Ffm/~/changes/64/develop/tutorials/integrating-aws-kinesis-data-firehose-with-glassflow)