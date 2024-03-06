# Mobility Tutorial for GlassFlow

This project focuses on creating a data pipeline using GlassFlow to process and analyze car-sharing (mobility) services data. The primary objectives include identifying low-fuel vehicles and finding the nearest fuel station based on GPS coordinates and fuel type. It also discounts drivers based on their vehicle's fuel level and proximity to the nearest fuel station.

In this set of tutorials, you'll find instructions on setting up the project, including prerequisites and steps for creating the pipeline, implementing data transformation functions, setting up data producers, and configuring data consumers.

Follow these steps to set up the mobility project.

## Prerequisites

Make sure that you have the following before proceeding with the installation:

- [Python is installed](https://www.python.org/downloads/) on your machine.
- [Pip](https://pip.pypa.io/en/stable/installation/) is installed to manage project packages.
- You created a [GlassFlow account](https://www.notion.so/o/aR82XtsD8fLEkzPmMtb7/s/pRyi93X0Jn9wrh2Z4Ffm/~/changes/9/get-started/create-account).
- You installed [GlassFlow CLI](https://www.notion.so/o/aR82XtsD8fLEkzPmMtb7/s/pRyi93X0Jn9wrh2Z4Ffm/~/changes/9/get-started/glassflow-cli) and logged into your account via the CLI.

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd tutorials/mobility
    ```
    
3. Create a new virtual environment:
    
    ```bash
    virtualenv venv && source venv/bin/activate
    ```
    
4. Install the required dependencies:
    
    ```
    pip install -r requirements.txt
    ```
    

## Steps

### 1. Create a Space via CLI

Open a terminal and create a new space called `examples` to organize multiple pipelines:

glassflow space create examples

Bash

After the space is created successfully, you will get a SpaceID in the terminal.

### 2. Create a Pipeline via CLI

Use the GlassFlow CLI to create a new data pipeline inside the space. 

```bash
glassflow pipeline create mobilitydemo --space=examples --function=transform.py
```

This command initializes the pipeline with a name `mobilitydemo` in the `examples` space and specifies the transformation function `transform.py`. After running the command, it returns a new **Pipeline ID** with its **Access Token**.

### 3. Create an environment configuration file

Add a `.env` file in the project directory and add the following configuration variables:

```bash
PIPELINE_ID=your_pipeline_id
SPACE_ID=your_space_id
PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
```

Replace `your_pipeline_id`, `your_space_id`, and `your_pipeline_access_token` with appropriate values obtained from your GlassFlow account.

### 4. Run data producer

Run the `producer_api.py` script to start publishing data:

```bash
python producer_api.py
```

### 5. Run data consumer

Run the `consumer_file.py` to retrieve transformed data from the pipeline:

```bash
python consumer_file.py
```

The script will start consuming data continuously from the pipeline and storing it locally on a .txt file. You can see an example of consumed data [here](https://github.com/glassflow/glassflow-examples/blob/main/tutorials/mobility/mobility_data_transformed.txt). You can further extend this functionality to push the consumed data to cloud storage buckets or real-time databases as per your project requirements.
