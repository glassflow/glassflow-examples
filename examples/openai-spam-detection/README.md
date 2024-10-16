# Spam Detection with OpenAI

This example showcases how to leverage OpenAI within the transform function and update the events data with the response. 
In this example, we will detect spam comments using OpenAI and add the result to the event. 

The entire process runs as a seververless event driven pipeline on GlassFlow. 

## Pre-requisites

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your [Personal Access Token](https://app.glassflow.dev/profile) to authorize the Python SDK to interact with GlassFlow Cloud.
- Get your OpenAI API Key https://platform.openai.com/