# GlassFlow and AWS Simple Queue Service (SQS) Integration Pipeline Example

This repository demonstrates how to integrate AWS SQS with GlassFlow to ingest and transform real-time data.

![GlassFlow AWS SQS](/assets/GlassFlow%20AWS%20SQS%20Integration.png)

## Prerequisites

To run the sample pipeline you'll need the following:

- [Python is installed](https://www.python.org/downloads/) on your machine.
- [Pip](https://pip.pypa.io/en/stable/installation/) is installed to manage project packages.
- You created a [GlassFlow account](https://www.notion.so/o/aR82XtsD8fLEkzPmMtb7/s/pRyi93X0Jn9wrh2Z4Ffm/~/changes/9/get-started/create-account).
- You installed [GlassFlow CLI](https://www.notion.so/o/aR82XtsD8fLEkzPmMtb7/s/pRyi93X0Jn9wrh2Z4Ffm/~/changes/9/get-started/glassflow-cli) and logged into your account via the CLI.
- You have an [AWS account](https://portal.aws.amazon.com/).
- You installed [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd tutorials/aws-sqs
    ```
3. Create a new virtual environment
Create a new virtual environment in the same folder and activate that environment:
    
    ```bash
    virtualenv glassflow && source glassflow/bin/activate
    ```

3. Install the GlassFlow, AWS Boto3 Python SDKs, and virtual environment package python-dotenvusing pip.

    ```bash
    pip install glassflow python-dotenv boto3
    ```

4. Read the following tutorial to learn how run the project: [Link to a tutorial].