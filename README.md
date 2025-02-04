<div align="center">
  <img src="https://gfassets.fra1.cdn.digitaloceanspaces.com/logo/logo-mono.png" /><br /><br />
</div>
<p align="center">
<a href="https://join.slack.com/t/glassflowhub/shared_invite/zt-2g3s6nhci-bb8cXP9g9jAQ942gHP5tqg">
        <img src="https://img.shields.io/badge/slack-join-community?logo=slack&amp;logoColor=white&amp;style=flat"
            alt="Chat on Slack"></a>


# GlassFlow Examples

This repository is your starting point for exploring examples and use cases for [GlassFlow](https://glassflow.dev).


## Pre-requisite

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your Personal Access Token to authorize the Python SDK to interact with GlassFlow Cloud from the [WebApp here](https://app.glassflow.dev/profile)
- Clone this repository to your local machine to access all the examples:
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```


## Explore

### Usage

Learn how to use the GlassFlow Python SDK:

* [Create Pipeline](usage/create_pipeline.ipynb): How to create a new pipeline.
* [Get Pipeline](usage/get_pipeline.ipynb): How to get information about an existing pipeline.
* [Manage Pipeline](usage/manage_pipeline.ipynb): How to update a pipeline and how to pause it.
* [Send and Receive events](usage/send_receive_events.ipynb): How to push and consume events to/from a pipeline.


### Examples

These are some basic examples that you can try with GlassFlow. The examples here should be familiar to you as a data engineer and will show you how GlassFlow works and how you can interact with it.

- [Hello World](examples/hello-world): Get started with GlassFlow with an hello world example 

- [Email Encryption](examples/email-encryption): Showcases how to hash email addresses (or other PII information) before sending them to your data warehouse.

- [Data Enrichment via API](examples/data-enrichment): Showcases how to call external API and enrich the data on the fly

- [Spam Detection with OpenAI](examples/openai-spam-detection): Showcases how to leverage openai API during the data transformation stage directly within the pipeline

- [PII detection and masking on unstructured data](examples/pii-detection-masking): Showcases how to do pii masking on unstructured data using hugging face 

- [Log format conversion](examples/opentel-log-transform): Showcases how to transform Open Telemetry log formats into a structure that can be ingested into ClickHouse.

- [Unstructured to structured data transformation](examples/unstructured-to-structured): Transform unstructured data like a YouTube video to extract key topics from the video transcript, generate additional insights, and translate the transcript into any specified language. 

- [Vector Embeddings](examples/vector-embeddings): An example on how to feed vector embeddings into your vector database.

- [Slack Alerting - Suspicious login](examples/slack-alerting): Use GlassFlow to send slack alert messages when there is a suspicious login

### Connectors

Here there are basic examples on how to create pipelines with our managed connectors:

- [Sources](connectors/source): Managed source connectors 
- [Sinks](connectors/sink): Managed sink connectors
- [Combination](connectors/combinations): Combination of source and sink connectors