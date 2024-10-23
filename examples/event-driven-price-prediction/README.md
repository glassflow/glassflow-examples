# Event-driven online price prediction

Many companies switching from batch processing to real-time processing to use dynamic data to make more relevant recommendations to customers. Static data are information that changes slowly or rarely – age, gender, job, neighborhood, etc. Dynamic data are information or action based on what’s happening right now – what you’re watching, what you’ve just liked on Instagram, you are searching for a taxi driver using Ubver, etc. Knowing a user’s interests right now will allow your systems to make recommendations much more relevant to them.

In this example, we will demonstrate a sample pipeline for **ride-hailing companies like Bolt or Uber** that can process data from two different microservices—Service A (Driver Availability) and Service B (Ride Demand), send events into ML model, and returns the best possible price to show customers in real-time each time they request a ride. Microservices—Service A, Service B, and Service C (prediction pipeline) communicates through an event-driven architecture where:

- Service A (Driver Availability): Manages driver availability in real-time.
- Service B (Ride Demand): Manages customer ride requests and demand in different regions.
- Service C (Price Prediction Pipeline): Predicts the best possible price for a ride based on driver availability and ride demand.

**Steps:**

1. Service A (Driver Availability) and Service B (Ride Demand) publish events to the same GlassFlow pipeline.
2. GlassFlow transformation function calculates predicted price based on the driver availability and ride demand.
3. The consumed output from the pipeline is visualized in real-time after receiving the price prediction event in Service C.

## Pre-requisites

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your [Personal Access Token](https://app.glassflow.dev/profile) to authorize the Python SDK to interact with GlassFlow Cloud.