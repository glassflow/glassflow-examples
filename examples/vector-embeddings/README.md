# Vector Embeddings
 
This example shows how to use GlassFlow to enrich events data with vector embeddings by calling an embeddings model endpoint.

## Pre-requisites

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your [Personal Access Token](https://app.glassflow.dev/profile) to authorize the Python SDK to interact with GlassFlow Cloud.
- Set up Vertex AI in GCP
    - Enable the VertexAI model you want to use (`text-embedding-004` in our case)    
    - Get your GCP service account credentials JSON with permissions `aiplatform.endpoints.predict`

