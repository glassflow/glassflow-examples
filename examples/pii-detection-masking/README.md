# PII Detection and Masking with Hugging Face

Do you have unstructured text where you need to detect and mask PII information? 

This example uses a Named Entity Model (NEM) from Hugging Face to detect PII and Llama processor to mask the PII information using the NEM output. 
The entire process runs as a seververless event driven pipeline on GlassFlow. 

## Pre-requisites

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your [Personal Access Token](https://app.glassflow.dev/profile) to authorize the Python SDK to interact with GlassFlow Cloud.
- Get your Hugging Face API token https://huggingface.co/