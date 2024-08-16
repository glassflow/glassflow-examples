# Generative Feedback Loop

TODO: Change use case description and create gif

In this example, we demonstrate how to 

user input for classified ads with [Langchain](https://www.langchain.com/) and save the results on [Redis](https://redis.io/). 

![Redis Dashbaord with Glassflow](/assets/Classified-Ads-enrichment-use-case.gif)

## Prerequisites

Make sure that you have the following before proceeding with the installation:

- [Sign up for a free GlassFlow account](http://app.glassflow.dev/).
- You have an account with [OpenAI API](https://openai.com/api/).
- Create an [API key](https://platform.openai.com/api-keys).
- You have an account with [Supabase](https://supabase.com/)
- You Have Supabase [API key](https://supabase.com/dashboard/project/_/settings/api)

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

### 1. Create a Space via WebApp

Navigate to the [Spaces page](https://app.glassflow.dev/spaces) and create a new space and called `examples` to organize multiple pipelines. 

### 2. Create a Pipeline via WebApp

Create a new data pipeline inside the space in the [Pipelines page](https://app.glassflow.dev/pipelines).

Follow the pipeline creation steps:
1. Specify the pipeline name `generative-feedback-loop` and select the space for it (`examples`)
2. Select Webhook data source
3. Upload `transform.py`
4. Choose openai library dependency from the Dependency menu
5. Select SDK data sink
6. Confirm pipeline creation and copy the new **Pipeline ID**, its **Access Token** and the **Webhook URL**

### 3. Create an environment configuration file

Add a `.env` file in the project directory and add the following configuration variables:

   ```bash
   PIPELINE_ID=your_pipeline_id
   PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
   SUPABASE_URL=https://<PROJECT_REF>.supabase.co
   SUPABASE_KEY=your_supabase_access_key
   OPENAI_API_KEY=your_openai_api_key
   ```

Set the supabase env variables, you can find your `PROJECT_REF` on your Supabase [project settings](https://supabase.com/dashboard/project/_/settings/general).
Set the `your_open_api_key`, replace `your_pipeline_id` and `your_pipeline_access_token` with appropriate values obtained from your GlassFlow account.


### 4. Run the project with Docker Compose:
    
   ```bash
   docker compose up
   ```

Docker compose will spin up:
- **Sink Connector**: With a small service that listens to your GlassFlow pipeline and saves the documents to the weaviate database
- **Weaviate DB**: weaviate server

### 5. Uncompress AirBnB New York listings

Uncompress the data:

   ```bash
   cd data
   tar -xzvf airbnb_vector_search.tar.gz
   ```

### 6. Create Supabase table and connect to pipeline webhook

1. [**Create new table**](https://supabase.com/dashboard/project/_/database/tables) 
   1. Enable Realtime checkbox
   2. Import data from Airbnb listings CSV
   3. Select ID as primary key
   4. Review auto-detected column types
   5. Add new column bool called `is_listing_in_weaviate`
2. [**Create new Webhook**](https://supabase.com/dashboard/project/_/database/hooks)
   1. Select previously created table
   2. Check **Insert** and **Update** events
   3. Paste your pipeline Webhook URL
   4. Add a new header **X-Pipeline-Access-Token** with your pipeline access token
3. [**Create access policies**](https://supabase.com/dashboard/project/_/auth/policies)
   1. Create a policy to enable select, insert and update for all users

### 7. Run producer
The producer will update the Airbnb listings column `is_listing_in_weaviate` and Supabase will send the updated row to GlassFlow:

   ```bash
   python producer.py
   ```

### 8. Search for accommodation

Open the streamlit search UI in your browser (https://localhost:8501) and search through the listings with natural language.
