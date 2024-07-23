# Classified Ads data enrichment

In this example, we demonstrate how to enrich user input for classified ads with [Langchain](https://www.langchain.com/) and save the results on [Redis](https://redis.io/). 

![Redis Dashbaord with Glassflow](/assets/Classified-Ads-enrichment-use-case.gif)

Follow these steps to run the pipeline.

## Prerequisites

Make sure that you have the following before proceeding with the installation:

- You created a [GlassFlow account](https://learn.glassflow.dev/docs/get-started/create-account).
- You installed [GlassFlow CLI](https://learn.glassflow.dev/docs/get-started/glassflow-cli) and logged into your account via the CLI.
- Basic knowledge of Langchain.

## Installation

We'll use the [GlassFlow WebApp](https://app.glassflow.dev/) to create a new space and configure the data pipeline.


1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd use-cases/classified-ads-data-enrichment
    ```

3. Create a new virtual environment:
    
    ```bash
    python -m venv .venv && source .venv/bin/activate
    ```
    
4. Install the required dependencies:
    
    ```
    pip install -r requirements.txt
    ```    

### Steps to run the GlassFlow pipeline

#### 1. Create a Space via WebApp

Navigate to the [Spaces page](https://app.glassflow.dev/spaces) and create a new space and called `examples` to organize multiple pipelines. 

![Create Space in GlassFlow WebApp](/assets/create-space-in-glassflow-webapp.png)

#### 2. Create a Pipeline via WebApp

Create a new data pipeline inside the space in the [Pipelines page](https://app.glassflow.dev/pipelines).

![Create Pipeline in GlassFlow WebApp](/assets/create-pipeline-in-glassflow-webapp-classified-ads-use-case.png)

Follow the pipeline creation steps:
1. Specify the pipeline name `classified-ads-enrichment` and select the space for it (`examples`)
2. Select SDK data source
3. Upload `transform.py`
4. Select SDK data sink
5. Confirm pipeline creation and copy the new **Pipeline ID** and its **Access Token**

#### 3. Create an environment configuration file

Add a `.env` file in the project directory and add the following configuration variables:

   ```bash
   PIPELINE_ID=your_pipeline_id
   PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
   ```

Replace `your_pipeline_id` and `your_pipeline_access_token` with appropriate values obtained from your GlassFlow account.

#### 6. Run the project with Docker Compose:
    
   ```bash
   docker compose up
   ```

Docker compose will spin up:
- **Sink Connector**: With a small service that listens to your GlassFlow pipeline and saves the documents to the redis database
- **Redis Stack**: redis server and [redis insight](http://localhost:8001/)

#### 7. Run producer

   ```bash
   python producer.py
   ```
