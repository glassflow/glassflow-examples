# Classified Ads enrichment

## Prerequisites

Make sure that you have the following before proceeding with the installation:

- You created a [GlassFlow account](https://learn.glassflow.dev/docs/get-started/create-account).
- You installed [GlassFlow CLI](https://learn.glassflow.dev/docs/get-started/glassflow-cli) and logged into your account via the CLI.
- Basic knowledge of Langchain.

## Installation

We'll use the [GlassFlow CLI](https://learn.glassflow.dev/docs/get-started/glassflow-cli) to create a new space and configure the data pipeline.


1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd use-cases/classified-ads-enrichment
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

#### 1. Create a Space via CLI

Open a terminal and create a new space called `examples` to organize multiple pipelines:

```bash
glassflow space create examples
```

After creating the space successfully, you will get a `SpaceID` in the terminal.

#### 2. Create a Pipeline via CLI

Create a new data pipeline inside the space.

```bash
glassflow pipeline create classified-ads-enrichment --space-id={space_id} --function=transform.py
```

This command initializes the pipeline with the name `classified-ads-enrichment` in the `examples` space and specifies the transformation function `transform.py`. After running the command, it returns a new **Pipeline ID** with its **Access Token**.

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
