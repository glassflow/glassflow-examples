# Postgres to Clickhouse data pipeline 

This minimal example shows how to setup a GlassFlow pipeline with `postgres` as data source and `clickhouse` as data sink. 

Both `postgres` and `clickhouse` are available as managed connectors within GlassFlow. 
You can read more about how to setup the connectors on our docs: 

[Postgres Docs](https://www.glassflow.dev/docs/integrations/sources/postgres-cdc)

[Clickhouse Docs](https://www.glassflow.dev/docs/integrations/sinks/clickhouse)



## Pre-requisite

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your [Personal Access Token](https://app.glassflow.dev/profile) to authorize the Python SDK to interact with GlassFlow Cloud.