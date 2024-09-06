<div align="center">
  <img src="https://docs.glassflow.dev/~gitbook/image?url=https%3A%2F%2F1082326815-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Forganizations%252FaR82XtsD8fLEkzPmMtb7%252Fsites%252Fsite_8vNM9%252Flogo%252Fft4nLD8mKhRmqTJjDp3i%252Flogo-color.png%3Falt%3Dmedia%26token%3Deb19e3bf-195b-413f-9965-4c76112953a3&width=128&dpr=3&quality=100&sign=10efaa8d&sv=1" /><br /><br />
</div>
<p align="center">
<a href="https://join.slack.com/t/glassflowhub/shared_invite/zt-2g3s6nhci-bb8cXP9g9jAQ942gHP5tqg">
        <img src="https://img.shields.io/badge/slack-join-community?logo=slack&amp;logoColor=white&amp;style=flat"
            alt="Chat on Slack"></a>

# GlassFlow Code Samples

This repository is your go-to resource for exploring the capabilities of GlassFlow through various end-to-end streaming data pipeline examples, starter kits, source and sink connector templates, sample data source generators.

## Explore

### Use-cases

- [Mobility data pipeline](use-cases/mobility/)
- [Real-time logs data anomaly detection with AI-powered transformation](use-cases/real-time-data-anomaly-detection/)
- [Real-time price recommendation with AI-powered transformation](use-cases/predict-car-price/)
- [Clickstream analytics dashboard](use-cases/clickstream-analytics-dashboard/)
- [Classified Ads data enrichment](use-cases/classified-ads-data-enrichment)

### End-to-end stream processing pipelines

- [GlassFlow, AWS Simple Queue Service (SQS) and AWS S3 Integration Pipeline Example](integrations/aws-sqs-s3/) - Integrate AWS SQS with GlassFlow to ingest, transform real-time data and write results to S3.
- [GlassFlow, AWS Kinesis Data Stream and AWS DynamoDB Integration Pipeline Example](integrations/aws-kinesis-dynamodb/) - Integrate AWS Kinesis Data Stream with GlassFlow to ingest, transform real-time data and write results to DynamoDB.
- [GlassFlow and Google Pub/Sub Integration Pipeline Example](integrations/google-pubsub/) - Integrate Google Cloud Pub/Sub with GlassFlow to ingest and transform real-time data.
- [GlassFlow, Azure Event Hubs and CosmosDB Integration Pipeline Example](integrations/azure-eventhub-cosmosdb/) - Integrate Azure Event Hubs and CosmosDB with GlassFlow to ingest and transform real-time data.

### Source Connectors

- [AWS Kinesis](/connectors/source/aws-kinesis)
- [AWS SQS](/connectors/source/aws-sqs)
- [Azure Event Hubs](/connectors/source/azure-event-hubs)
- [Google Pub/Sub](/tutorials/google-pubsub/pubsub_subscriber.py)

### Sink Connectors

- [AWS DynamoDB](/connectors/sink/aws-dynamodb/)
- [AWS S3](/connectors/sink/aws-s3)
- [Azure CosmosDB](/connectors/sink/azure-cosmosdb)
- [Redis](/connectors/sink/redis)


### Getting Started

1. Start cloning this repository to your local machine to access all the integrations and use cases.
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate through the repository to find examples that match your interests.
    
    ```bash
    cd use-cases
    ```
3. Visit the developer documentation for more information: https://docs.glassflow.dev
