# Integrating AWS Kinesis Stream and DynamoDB with GlassFlow

This example project demonstrates how to build an end-to-end serverless streaming data pipeline with AWS Kinesis Data Streams, GlassFlow and AWS DynamoDB.

![Data pipeline with Amazon Kinesis Data Streams, DynamoDB and GlassFlow](/assets/AWS-kinesis-dynamodb.png)

## Prerequisites

To run the sample pipeline, you'll need the following:

- [Docker](https://www.docker.com/get-started) is installed on your machine
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
    cd tutorials/aws-kinesis-dynamodb
    ```

3. Read the following tutorial to learn how to run the GlassFlow and obtain `PIPELINE_ID` and `PIPELINE_ACCESS_TOKEN` values: [Integrating AWS Kinesis and DynamoDB with GlassFlow](https://learn.glassflow.dev/docs/develop/tutorials/integrating-aws-kinesis-data-streams-and-dynamodb-with-glassflow)

4. Create a `.env` file in the same project directory and fill it with the following environment variables:

    ```
    AWS_ACCESS_KEY_ID=your_access_key_id
    AWS_SECRET_ACCESS_KEY=your_secret_access_key
    AWS_KINESIS_STREAM_NAME=your_kinesis_stream_name
    AWS_DYNAMODB_TABLE_NAME=your_dynamodb_table_name
    AWS_REGION=your_aws_region
    PIPELINE_ID=your_pipeline_id
    PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
    ```

5. Run the project with Docker Compose:
    
    ```bash
    docker compose up
    ```

## Environment Variables

Before running the project, ensure you have set the following environment variables:

| Variable Name           | Description                              |
|-------------------------|------------------------------------------|
| AWS_ACCESS_KEY_ID       | Your AWS access key ID                   |
| AWS_SECRET_ACCESS_KEY   | Your AWS secret access key               |
| AWS_KINESIS_STREAM_NAME | The name of your AWS Kinesis stream      |
| AWS_DYNAMODB_TABLE_NAME | The name of your AWS DynamoDB table      |
| AWS_REGION              | The AWS region where your resources are located |
| PIPELINE_ID             | Your GlassFlow pipeline ID               |
| PIPELINE_ACCESS_TOKEN   | Your GlassFlow pipeline access token     |
