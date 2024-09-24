# Integrating Azure Event Hubs and CosmosDB with GlassFlow

This example project demonstrates how to build an end-to-end serverless streaming data pipeline with Azure Event Hubs and CosmosDB.


## Prerequisites

To run the sample pipeline, you'll need the following:

- [Docker](https://www.docker.com/get-started) installed on your machine.
- You created a [GlassFlow account](https://learn.glassflow.dev/docs/get-started/create-account#create-a-new-account), installed the [GlassFlow CLI](https://learn.glassflow.dev/docs/get-started/glassflow-cli#installation), and logged into your account via the CLI.
- Microsoft Azure subscription. To use Azure services, including Azure Event Hubs and CosmosDB, you need a subscription. If you don't have an existing Azure account, sign up for a [free trial](https://azure.microsoft.com/en-gb/free/).
- You installed the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

## Azure Resource Creation

Before running the project, you need to create the required Azure resources. Execute the following commands in your terminal to create the resources using Azure CLI:

```bash
RESOURCE_GROUP=test-streaming
EVENT_HUB_NAMESPACE=taxidataeventshubspace
EVENT_HUB_NAME=taxi-data-events
EVENT_HUB_AUTHORIZATION_RULE=taxi-data-event-produce-consume-permit
STORAGE_ACCOUNT=taxidataeventstorage
BLOB_CONTAINER=taxixatablob
COSMOS_DB_ACCOUNT=taxidatadbaccount
COSMOS_DB_NAME=taxidatadb
COSMOS_DB_CONTAINER_NAME=taxidatadbcontainer
LOCATION=eastus

az login

az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

az eventhubs namespace create \
    --resource-group $RESOURCE_GROUP \
    --name $EVENT_HUB_NAMESPACE
az eventhubs eventhub create \
    --resource-group $RESOURCE_GROUP \
    --name $EVENT_HUB_NAME \
    --namespace-name $EVENT_HUB_NAMESPACE
az eventhubs eventhub authorization-rule create \
    --resource-group $RESOURCE_GROUP \
    --name $EVENT_HUB_AUTHORIZATION_RULE \
    --eventhub-name $EVENT_HUB_NAME \
    --namespace-name $EVENT_HUB_NAMESPACE \
    --rights Listen Send
    
AZURE_EVENT_HUB_CONNECTION_STRING=$( \
    az eventhubs eventhub authorization-rule keys list \
        --resource-group $RESOURCE_GROUP \
        --name $EVENT_HUB_AUTHORIZATION_RULE \
        --eventhub-name $EVENT_HUB_NAME \
        --namespace-name $EVENT_HUB_NAMESPACE \
        --query primaryConnectionString \
        --output tsv)
        
echo $AZURE_EVENT_HUB_CONNECTION_STRING

az storage account create \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --name $STORAGE_ACCOUNT \
    --sku Standard_LRS

az storage container create \
    --account-name $STORAGE_ACCOUNT \ 
    --name $BLOB_CONTAINER \
    --auth-mode login

AZURE_STORAGE_CONNECTION_STRING=$( \
    az storage account show-connection-string \
        --name $STORAGE_ACCOUNT \
        --query connectionString \
        --output tsv)
        
echo $AZURE_STORAGE_CONNECTION_STRING

az cosmosdb create \
    --resource-group $RESOURCE_GROUP \
    --name $COSMOS_DB_ACCOUNT
    
AZURE_COSMOSDB_CONNECTION_STRING=$( \
    az cosmosdb keys list \
        --resource-group $RESOURCE_GROUP \
        --name $COSMOS_DB_ACCOUNT \
        --type connection-strings \
        --query connectionStrings[0].connectionString \
        --output tsv)
echo $AZURE_COSMOSDB_CONNECTION_STRING
```

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
2. Navigate to the project directory:
    
    ```bash
    cd tutorials/azure-eventhub-cosmosdb
    ```

3. Create a space and pipeline using [GlassFlow CLI](https://learn.glassflow.dev/docs/get-started/glassflow-cli#key-commands) to obtain `PIPELINE_ID` and `PIPELINE_ACCESS_TOKEN` values:

    ```bash
    cd pipeline
    glassflow space create myspace
    glassflow pipeline create taxi_data_process_pipeline —space-id={your_space_id} --function=transform.py
    ```

4. Create a `.env` file in the same project directory and fill it with the following environment variables:

    ```
    AZURE_EVENT_HUB_NAME=your_event_hub_name
    AZURE_EVENT_HUB_CONNECTION_STRING=your_event_hub_connection_string
    AZURE_EVENT_HUB_CONSUMER_GROUP=your_consumer_group
    AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string
    AZURE_STORAGE_BLOB_CONTAINER_NAME=your_blob_container_name
    AZURE_COSMOS_DB_NAME=your_cosmosdb_name
    AZURE_COSMOS_CONTAINER_NAME=your_cosmosdb_container_name
    AZURE_COSMOSDB_CONNECTION_STRING=your_cosmosdb_connection_string
    PIPELINE_ID=your_pipeline_id
    PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
    ```

5. Run the project with Docker Compose:
    
    ```bash
    docker compose up
    ```

## Environment Variables

Before running the project, ensure you have set the following environment variables:

| Variable Name                   | Description                              |
|---------------------------------|------------------------------------------|
| AZURE_EVENT_HUB_NAME            | Your Azure Event Hub name                |
| AZURE_EVENT_HUB_CONNECTION_STRING | Your Azure Event Hub connection string |
| AZURE_EVENT_HUB_CONSUMER_GROUP  | Your Azure Event Hub consumer group      |
| AZURE_STORAGE_CONNECTION_STRING | Your Azure Storage connection string     |
| AZURE_STORAGE_BLOB_CONTAINER_NAME | The name of your Azure Blob Storage container |
| AZURE_COSMOS_DB_NAME            | Your Azure Cosmos DB name                |
| AZURE_COSMOS_CONTAINER_NAME     | Your Azure Cosmos DB container name      |
| AZURE_COSMOSDB_CONNECTION_STRING | Your Azure Cosmos DB connection string  |
| PIPELINE_ID                     | Your GlassFlow pipeline ID               |
| PIPELINE_ACCESS_TOKEN           | Your GlassFlow pipeline access token     |
