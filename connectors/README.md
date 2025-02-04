<div align="center">
  <img src="https://gfassets.fra1.cdn.digitaloceanspaces.com/logo/logo-mono.png" /><br /><br />
</div>

# Managed Connectors

This folder contains minimal examples on how to configure managed source and sink connectors with the Python SDK.

## Sources

- [Amazon SQS](source/amazon-sqs)
- [Google PubSub](source/google-pubsub)
- [Postgres](source/postgres)

## Sinks

- [Amazon S3](sink/amazon-s3)
- [Clickhouse](sink/clickhouse)
- [Pinecone](sink/pinecone)
- [Snowflake](sink/snowflake)
- [Webhook](sink/webhook)

## Combinations

- [Postgres → Clickhouse](combinations/postgres-clickhouse)
- [Postgres → Snowflake](combinations/postgres-snowflake)
- [Amazon SQS → Amazon S3](combinations/amazon-sqs-amazon-s3)
