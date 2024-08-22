# Generative Feedback Loop

In this example, we demonstrate how to use GlassFlow to connect changes in your [Supabase](https://supabase.com/) 
database to a vector database ([Weaviate](https://weaviate.io/)) and perform semantic search.

## Prerequisites

Make sure that you have the following before proceeding with the installation:

- [Sign up for a free GlassFlow account](http://app.glassflow.dev/).
- You have an account with [OpenAI API](https://openai.com/api/).
- Create an [API key](https://platform.openai.com/api-keys).
- You have a [Supabase](https://supabase.com/) account.
- You have an account on Weaviate and have the REST endpoint url and the API key (https://console.weaviate.cloud/dashboard).

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd use-cases/generative-feedback-loop
    ```

3. Create a new virtual environment:
    
    ```bash
    python -m venv .venv && source .venv/bin/activate
    ```
    
4. Install the required dependencies:
    
    ```
    pip install -r requirements.txt
    ```    

## Steps to create the GlassFlow pipeline

We'll use the [GlassFlow WebApp](https://app.glassflow.dev/) to create a new space and configure the data pipeline.

### 1. Create Weaviate collection

Create a new collection called `AirbnbNYC` and choose a vectorizer to match the one used in your transformation. In our
case is `text2vec-openai` and model `text-embedding-3-small`.

### 2. Create a Space via WebApp

Navigate to the [Spaces page](https://app.glassflow.dev/spaces) and create a new space and called `examples` to organize multiple pipelines.

### 3. Create a Pipeline via WebApp

Create a new data pipeline inside the space in the [Pipelines page](https://app.glassflow.dev/pipelines).

Follow the pipeline creation steps:
1. Specify the pipeline name `generative-feedback-loop` and select the space for it (`examples`)
2. Select Webhook data source
3. Upload `transform.py`
4. Choose openai library dependency from the Dependency menu
5. Select Webhook data sink and fill the URL and headers:
   1. URL: `https://${WEAVIATE_INSTANCE_URL}/v1/objects`
   2. Headers:
      - `Content-Type`: `application/json`
      - `Authentication`: `Bearer ${WEAVIATE_API_KEY}`
6. Confirm pipeline creation and copy the new **Pipeline ID**, its **Access Token** and the **Webhook URL**

### 4. Create Supabase table

Create a new table on Supabase with the following configuration:
 - Enable realtime
 - Disable Row Level Security (Or create a policy to allow SELECT and INSERT to `public` schema)
 - Add schema definition

### 5. Create webhook trigger on Supabase

Follow [the instructions from Supabase](https://supabase.com/docs/guides/database/webhooks#creating-a-webhook) to 
create the webhook and hook it to `INSERT` events on your table. Use the pipeline webhook URL from your 
pipeline's details page and add the following headers `X-Pipeline-Access-Token` and `Content-Type`.


### 6. Populate Supabase database

To test the pipeline, we can create some rows in our Supabase table by running the command:

   ```bash
   python populate_supabase.py 100
   ```

This will insert the first 100 rows from the Airbnb dataset into the database which will trigger the data to be sent 
to Weaviate.

**Note**: Make sure to fill your Supabase URL and API Key in the `.env` file.

### 7. Search your database

You can now search your Weaviate database on the [search console](https://console.weaviate.cloud/apps/query/).
