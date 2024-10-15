# Email Encryption


This example showcases how to use GlassFlow to transform your user data in motion.

Quite often, the event data that teams ingest includes email addresses. As a data engineer, you want to store the email addresses in the data warehouse, but not in plain text.

In this example, we encrypt the email address from the input data on the fly by applying a transformation function.

With GlassFlow, we only need to publish the transform code, and GlassFlow automatically runs the function on every input event.


## Pre-requisite

- CCreate your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your [Personal Access Token](https://app.glassflow.dev/profile) to authorize the Python SDK to interact with GlassFlow Cloud.