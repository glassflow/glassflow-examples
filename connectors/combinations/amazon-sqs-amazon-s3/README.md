# Move data from Amazon SQS to Amazon S3 

This example showcases how to move data from amazon SQS topic into an amazon S3 bucket using GlassFlow. 

More details on how to setup a Amazon SQS connector can be found on [SQS docs](https://www.glassflow.dev/docs/integrations/sources/amazon-sqs)

For details on setting up a Amazon S3 connector, see [S3 docs](https://www.glassflow.dev/docs/integrations/sinks/amazon-s3)

For a list of all managed connectors available, see [integrations docs](https://www.glassflow.dev/docs/integrations)


## Pre-requisite

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your [Personal Access Token](https://app.glassflow.dev/profile) to authorize the Python SDK to interact with GlassFlow Cloud.

## Setting up the pipeline 

1. Create a local python environment and install `glassflow` python package 

`pip install glassflow`

2. Fill out sqs and s3 connector details in the file `pipeline.py`. You will run this file locally to create the pipeline. 

3. Run the `pipeline.py` locally which uses glassflow python SDK to create the pipeline

```python pipeline.py```

