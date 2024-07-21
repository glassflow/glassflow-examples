import json
import random
import pandas as pd


def handler(data, log):
    log.info("Event:" + json.dumps(data), data=data)

    booking_timestamp = pd.Timestamp(data["booking_timestamp"])

    # Get the day of the week
    day_of_week = booking_timestamp.strftime("%A")

    # Get weather conditions
    weather_conditions = random.choice(
        ["clear", "rainy", "snowy", "cloudy", "sunny", "windy"]
    )

    # Get traffic conditions
    traffic_conditions = random.choice(["light", "moderate", "heavy", "normal"])

    # Generate passenger pick-up time
    passenger_pick_up_time = booking_timestamp + pd.Timedelta(
        minutes=random.randint(1, 30)
    )

    # Generate a random additional waiting time before cancellation (1 to 10 minutes)
    additional_waiting_time = random.randint(1, 10)

    # Get other required data from event_data
    drivers_review = data["drivers_review"]
    estimated_arrival_time = data["estimated_arrival_time_in_m"]
    time_of_day = booking_timestamp.hour
    booking_source = data["booking_source"]
    trip_duration = data["trip_duration"]

    # Introduce patterns for cancellations
    if (
        drivers_review < 2
        or estimated_arrival_time > (estimated_arrival_time + additional_waiting_time)
        or (
            time_of_day == "morning"
            and 6.5 <= booking_timestamp.hour <= 9
            and estimated_arrival_time > random.randint(1, 10)
        )
    ) and (
        weather_conditions == "rainy"
        or time_of_day == "night"
        or day_of_week in ["Saturday", "Sunday"]
        or booking_source == "app"
    ):
        status = "cancelled"
        cancelled_time = booking_timestamp + pd.Timedelta(minutes=random.randint(1, 10))
        # Order completion time for cancellations
        order_completion_time = cancelled_time
        passenger_pick_up_time = None
        trip_duration = None
    else:
        status = "completed"
        cancelled_time = None
        order_completion_time = booking_timestamp + pd.Timedelta(minutes=trip_duration)
        passenger_pick_up_time = booking_timestamp + pd.Timedelta(
            minutes=(estimated_arrival_time + random.randint(-5, 5))
        )
        trip_duration = order_completion_time - passenger_pick_up_time

    data["day_of_week"] = day_of_week
    data["weather_conditions"] = weather_conditions
    data["traffic_conditions"] = traffic_conditions
    data["passenger_pick_up_time"] = str(passenger_pick_up_time)
    data["status"] = status
    data["order_completion_time"] = str(order_completion_time)

    return data

