# Real-time car price data recommendation pipeline using AI

This example streaming data pipeline with GlassFlow demonstrates how to monitor real-time car data events
and predict future prices using OpenAI.

Follow these steps to run the pipeline.

## Prerequisites

Make sure that you have the following before proceeding with the installation:

- You created a [GlassFlow account](https://learn.glassflow.dev/docs/get-started/create-account).
- You installed [GlassFlow CLI](https://learn.glassflow.dev/docs/get-started/glassflow-cli) and logged into your account via the CLI.
- You have [OpenAI API](https://openai.com/api/) account.

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd use-cases/predict-car-price
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

#### 1. Get a new OpenAI API Key

 Create [API key](https://platform.openai.com/api-keys) to use [OpenAI API](https://platform.openai.com/docs/api-reference/authentication) endpoints.

#### 2. Set OpenAI API Key

Open the `transform.py` file and replace `{REPLACE_WITH_YOUR_OPENAI_API_KEY}` with your API key.

#### 3. Create a Space via CLI

Open a terminal and create a new space called `examples` to organize multiple pipelines:

```bash
glassflow space create examples
```

After creating the space successfully, you will get a SpaceID in the terminal.

#### 4. Create a Pipeline via CLI

Use the GlassFlow CLI to create a new data pipeline inside the space. 

```bash
glassflow pipeline create predict-car-price --space-id={space_id} --function=transform.py --requirements=openai
```

This command initializes the pipeline with the name `predict-car-price` in the `examples` space and specifies the transformation function `transform.py`. After running the command, it returns a new **Pipeline ID** with its **Access Token**.

#### 5. Create an environment configuration file

Add a `.env` file in the project directory and add the following configuration variables:

```bash
PIPELINE_ID=your_pipeline_id
SPACE_ID=your_space_id
PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
```

Replace `your_pipeline_id`, `your_space_id`, and `your_pipeline_access_token` with appropriate values obtained from your GlassFlow account.

#### 6. Run data producer

Run the `producer.py` script to start publishing data:

```bash
python producer.py
```

#### 7. Run data consumer

Run the `consumer.py` to retrieve transformed data from the pipeline:

```bash
python consumer.py
```
