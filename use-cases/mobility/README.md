# Mobility Project Example Pipeline

This project focuses on creating a data pipeline using GlassFlow to process and analyze car-sharing (mobility) services data. The primary objectives include identifying low-fuel vehicles and finding the nearest fuel station based on GPS coordinates and fuel type. It also discounts drivers based on their vehicle's fuel level and proximity to the nearest fuel station.


![GlassFlow car sharing pipeline](/assets/GlassFlow%20car%20sharing%20pipeline.png)

## Prerequisites

To start with this setup, you need a free GlassFlow account.

- [Sign up for a free account](http://app.glassflow.dev/)
- [Python is installed](https://www.python.org/downloads/) on your machine.
- [Download and install Pip](https://pip.pypa.io/en/stable/installation/) to manage project packages.

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd use-cases/mobility
    ```
    
3. Create a new virtual environment:
    
    ```bash
    python -m venv .venv && source .venv/bin/activate
    ```
    
4. Install the required dependencies:
    
    ```
    pip install -r requirements.txt
    ```
    

## Setting Up the Pipeline with GlassFlow

Follow the [easy steps in the tutorial](https://docs.glassflow.dev/tutorials/use-cases/mobility-project) to create a pipeline using GlassFlow WebApp.

## Run data producer

Run the `producer_api.py` script to start publishing data:

```bash
python producer_api.py
```

## Run data consumer

Run the `consumer_file.py` to retrieve transformed data from the pipeline:

```bash
python consumer_file.py
```

The script will start consuming data continuously from the pipeline and storing it locally on a .txt file. You can see an example of consumed data `mobility_data_transformed.txt`. You can further extend this functionality to push the consumed data to cloud storage buckets or real-time databases as per your project requirements.

You can also find instructions on how to run the example project [in the GlassFlow docs](https://docs.glassflow.dev/tutorials/use-cases/mobility-project).