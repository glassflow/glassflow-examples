import pandas as pd
from collections import defaultdict

# In-memory storage to hold the latest events from each service
event_cache = defaultdict(dict)


# GlassFlow mandatory handler function
def handler(data, log):
    """
    The GlassFlow handler function processes driver availability and ride demand data,
    calculates price predictions, and returns the transformed data.

    Parameters:
    - data: Incoming event data from both Service A (driver availability) and Service B (ride demand).
    - log: Logging object for logging within the pipeline.

    Returns:
    - A dictionary containing predicted price and other related information.
    """
    try:
        log.info("Starting price prediction transformation")

        global event_cache

        # Ensure the incoming data is a list
        if isinstance(data, dict):
            data = [data]

        # Update the event cache with the incoming data
        for event in data:
            if not isinstance(event, dict):
                log.error(f"Invalid event format: {event}")
                continue

            region = event.get("region")
            event_type = event.get("event")

            if region and event_type:
                if event_type == "driver_availability":
                    event_cache[region]["availability_data"] = event
                elif event_type == "ride_demand":
                    event_cache[region]["demand_data"] = event
            else:
                log.error(f"Missing region or event type in event: {event}")

        results = []

        # Iterate through the cache to check if both driver availability and ride demand data are present
        for region, events in event_cache.items():
            availability_data = events.get("availability_data")
            demand_data = events.get("demand_data")

            # If both pieces of information are available, compute the price
            if availability_data and demand_data:
                try:
                    available_drivers = availability_data["available_drivers"]
                    ride_requests = demand_data["ride_requests"]
                    base_price = 5.00
                    demand_factor = ride_requests / available_drivers

                    # Simple price prediction logic based on driver availability and demand
                    # You can replace it with a more sophisticated ML model
                    predicted_price = base_price * demand_factor

                    # Build the result
                    result = {
                        "region": region,
                        "predicted_price": round(predicted_price, 2),
                        "available_drivers": available_drivers,
                        "ride_requests": ride_requests,
                        "datetime": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }

                    log.info(f"Price prediction computed: {result}")
                    results.append(result)

                    # Clear the processed events for this region from the cache
                    event_cache[region] = {}

                except KeyError as e:
                    log.error(f"Missing key in event data: {e}")
                    continue

        if results:
            return {"predicted_price": results}
        else:
            log.info("Insufficient data for price prediction")
            return {"predicted_price": []}

    except Exception as e:
        log.error(f"Error during transformation: {e}")
        raise
