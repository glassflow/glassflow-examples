<div align="center">
  <img src="https://learn.glassflow.dev/~gitbook/image?url=https:%2F%2F3630921082-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FpRyi93X0Jn9wrh2Z4Ffm%252Flogo%252Fj4ZLY66JC4CCI0kp4Tcl%252FBlue.png%3Falt=media%26token=824ab2c7-e9a7-4b53-bd9a-375650951fc1&width=128&dpr=2&quality=100&sign=312af88abf1a93b897726483f4d86c2733192ab70b94b68ba438f6c85caf7e1a" /><br /><br />
</div>
<p align="center">
<a href="https://join.slack.com/t/glassflowhub/shared_invite/zt-2g3s6nhci-bb8cXP9g9jAQ942gHP5tqg">
        <img src="https://img.shields.io/badge/slack-join-community?logo=slack&amp;logoColor=white&amp;style=flat"
            alt="Chat on Slack"></a>

# GlassFlow Code Samples

This repository is your go-to resource for exploring the capabilities of GlassFlow through various end-to-end streaming data pipeline examples, starter kits, source and sink connector templates, sample data source generators.

## Explore

### End-to-end stream processing pipelines

- [GlassFlow, AWS Simple Queue Service (SQS) and AWS S3 Integration Pipeline Example](tutorials/aws-sqs-s3/) - Integrate AWS SQS with GlassFlow to ingest, transform real-time data and write results to S3.
- [GlassFlow, AWS Kinesis Data Stream and AWS DynamoDB Integration Pipeline Example](tutorials/aws-kinesis-dynamodb/) - Integrate AWS Kinesis Data Stream with GlassFlow to ingest, transform real-time data and write results to DynamoDB.
- [Mobility data pipeline](tutorials/mobility/) - Creating a data pipeline using GlassFlow to process and analyze car-sharing (mobility) services data.
- [GlassFlow and Google Pub/Sub Integration Pipeline Example](tutorials/google-pubsub/) - Integrate Google Cloud Pub/Sub with GlassFlow to ingest and transform real-time data.
- [GlassFlow, Azure Event Hubs and CosmosDB Integration Pipeline Example](tutorials/azure-eventhub-cosmosdb/) - Integrate Azure Event Hubs and CosmosDB with GlassFlow to ingest and transform real-time data.

### Use-cases

- [AI-powered transformation for real-time logs data anomaly detection](use-cases/real-time-data-anomaly-detection/)
- [Real-time car price data recommendation pipeline](use-cases/predict-car-price/)

### Source Connectors

- [AWS Kinesis](/connectors/source/aws-kinesis)
- [AWS SQS](/connectors/source/aws-sqs)
- [Azure Event Hubs](/connectors/source/azure-event-hubs)
- [Google Pub/Sub](/tutorials/google-pubsub/pubsub_subscriber.py)

### Sink Connectors

- [AWS DynamoDB](/connectors/sink/aws-dynamodb/)
- [AWS S3](/connectors/sink/aws-s3)
- [Azure CosmosDB](/connectors/sink/azure-cosmosdb)


### Getting Started

1. Start with cloning this repository to your local machine to access all the examples and resources.
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate through the repository to find examples that match your interests or use case.
    
    ```bash
    cd tutorials
    ```
3. Visit the developer documentation for more information: https://learn.glassflow.dev/docs
