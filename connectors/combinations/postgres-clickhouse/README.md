# Postgres to ClickHouse data pipeline 

This example showcases how to move data from postgres to Clickhouse using GlassFlow. 

More details on how to setup a Postgres connector can be found on [postgres docs](https://www.glassflow.dev/docs/integrations/sources/postgres-cdc)

For details on setting up a ClickHouse connector, see [Clickhouse Docs](https://www.glassflow.dev/docs/integrations/sinks/clickhouse)

For a list of all managed connectors available, see [integrations docs](https://www.glassflow.dev/docs/integrations)


## Pre-requisite

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your [Personal Access Token](https://app.glassflow.dev/profile) to authorize the Python SDK to interact with GlassFlow Cloud.

## Setting up the pipeline 

1. Create a local python environment and install `glassflow` python package 

`pip install glassflow`

2. Fill out postgres and clickhouse connector details in the file `pipeline.py`. You will run this file locally to create the pipeline. 

3. Run the `pipeline.py` locally which uses glassflow python SDK to create the pipeline

```python pipeline.py```

