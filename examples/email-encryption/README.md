# Email Encryption


This examples showcases how to use GlassFlow to transform your user data in motion.

Quite often the events data that the team ingests consists of email addresses. As a data engineer, you want to put the email address on the data-warehouse but not in plain-text.

In this example, we encrypt the email address from the input data on the fly by applying a transformation function.

With glassflow, we only need to publish the transform code and glassflow automatically runs the function on every input event.


## Pre-requisite

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev)
- Get your Personal Access Token to authorize the python sdk to interact with GlassFlow Cloud