# AI transformation for real-time data anomaly detection

This example transformation demontrates data anomaly detection with GlassFlow and OpenAI to monitor server logs to detect unusual patterns or suspicious activities.

Follow these steps to run the transformation function.

## Prerequisites

Make sure that you have the following before proceeding with the installation:

- [Python is installed](https://www.python.org/downloads/) on your machine.
- [Pip](https://pip.pypa.io/en/stable/installation/) is installed to manage project packages.
- You created a [GlassFlow account](https://www.notion.so/o/aR82XtsD8fLEkzPmMtb7/s/pRyi93X0Jn9wrh2Z4Ffm/~/changes/9/get-started/create-account).
- You installed [GlassFlow CLI](https://www.notion.so/o/aR82XtsD8fLEkzPmMtb7/s/pRyi93X0Jn9wrh2Z4Ffm/~/changes/9/get-started/glassflow-cli) and logged into your account via the CLI.
- You have [OpenAI API](https://openai.com/api/) account.

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd transformations/ai
    ```
    
3. Create a new virtual environment:
    
    ```bash
    virtualenv venv && source venv/bin/activate
    ```
    
4. Install the required dependencies:
    
    ```
    pip install -r requirements.txt
    ```

## Steps to run GlassFlow pipeline

### 1. Get a new OpenAI API Key

 Create [API key](https://platform.openai.com/api-keys) to use [OpenAI API](https://platform.openai.com/docs/api-reference/authentication) endpoints.

### 2. Set OpenAI API Key

Open `transform.py` file and replace `{REPLACE_WITH_YOUR_OPENAI_API_KEY}` with your actual API key.

### 3. Create a Space via CLI

Open a terminal and create a new space called `examples` to organize multiple pipelines:

```bash
glassflow space create examples
```

After the space is created successfully, you will get a SpaceID in the terminal.

### 4. Create a Pipeline via CLI

Use the GlassFlow CLI to create a new data pipeline inside the space. 

```bash
glassflow pipeline create anomalies-detection --space-id={space_id} --function=transform.py
```

This command initializes the pipeline with a name `anomalies-detection` in the `examples` space and specifies the transformation function `transform.py`. After running the command, it returns a new **Pipeline ID** with its **Access Token**.

### 5. Create an environment configuration file

Add a `.env` file in the project directory and add the following configuration variables:

```bash
PIPELINE_ID=your_pipeline_id
SPACE_ID=your_space_id
PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
```

Replace `your_pipeline_id`, `your_space_id`, and `your_pipeline_access_token` with appropriate values obtained from your GlassFlow account.

### 6. Run data generator

Run the `generator.py` script to start publishing fake server logs data to the GlassFlow:

```bash
python generator.py
```

### 7. Run data consumer

Run the `consumer.py` to retrieve transformed logs data from the GlassFlow pipeline:

```bash
python consumer.py
```