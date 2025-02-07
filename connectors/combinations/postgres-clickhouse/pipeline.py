import glassflow
personal_access_token = ""

# POSTGRES PARAMETERS
# Please see docs at https://www.glassflow.dev/docs/integrations/sources/postgres-cdc on how to setup the parameters
POSTGRES_HOST = "" # host of IP address
POSTGRES_PORT = "" # port, typically 5432
POSTGRES_USER = "" # user
POSTGRES_PASSWORD = "" # password
POSTGRES_DB_NAME = "" # database name
REPLICATION_SLOT = "" # replication slot created on database from which cdc reads the changes. See docs for details on setting this on postgres
REPLICATION_PLUGIN_ARGS = "" # additional arguments for the plugin wall2json, ignore if nothing additional needed


# CLICKHOUSE PARAMETERS 
CLICKHOUSE_ADDRESS = "" # glassflow uses native protocol. this should be of format xxyy.europe-west4.gcp.clickhouse.cloud:9440
CLICKHOUSE_DATABASE = "" # database where the table is 
CLICKHOUSE_USERNAME = "" # username
CLICKHOUSE_PASSWORD = "" # password
CLICKHOUSE_TABLE = "" # table where to insert the data

client = glassflow.GlassFlowClient(
    personal_access_token=personal_access_token
)

# create a space to put the pipeline 
space = client.create_space(name="postgres-pipelines")
space_id = space.id
pipeline_name = "postgres-to-clickhouse"
transformation_file = "transform.py" # location of the file where the transformation code is 

pipeline = client.create_pipeline(
    name=pipeline_name, 
    transformation_file=transformation_file,
    space_id=space_id, 
    source_kind="postgres",
    source_config={
        "db_host": POSTGRES_HOST,
        "db_port": POSTGRES_PORT,
        "db_user": POSTGRES_USER,
        "db_pass": POSTGRES_PASSWORD,
        "db_name": POSTGRES_DB_NAME,
        "replication_slot": REPLICATION_SLOT
    },
    sink_kind="clickhouse",
    sink_config={
        "addr": CLICKHOUSE_ADDRESS,
        "database": CLICKHOUSE_DATABASE,
        "username": CLICKHOUSE_USERNAME,
        "password": CLICKHOUSE_PASSWORD,
        "table": CLICKHOUSE_TABLE,
    }
)
print("Pipeline ID:", pipeline.id)
print("Explore your pipeline on the web UI at", "https://app.glassflow.dev/pipelines/{}/logs".format(pipeline.id))
