import json


def handler(data, log):
    log.info("Event received: " + json.dumps(data))

    # Example dimensions received from Google Analytics
    country = data.get("country")
    city = data.get("city")
    device_category = data.get("deviceCategory")
    screen_name = data.get("unifiedScreenName")
    screen_page_views = data.get("screenPageViews", 0)
    event_count = int(data.get("eventCount", 0))
    screen_page_views = int(data.get("screenPageViews", 0))
    active_users = int(data.get("activeUsers", 0))

    # Compute engagement score
    engagement_score = (event_count + screen_page_views) / (
        active_users + 1
    )  # Adding 1 to avoid division by zero

    # Device usage insights
    device_usage = {"desktop": 0, "mobile": 0, "tablet": 0}
    device_usage[device_category] += 1

    # Content popularity
    content_popularity = {
        screen_name: {
            "event_count": event_count,
            "screen_page_views": screen_page_views,
        }
    }

    # Geographic distribution
    geographic_distribution = {country: {"city": city, "active_users": active_users}}

    # Add computed insights to data
    data.update(
        {
            "engagement_score": engagement_score,
            "device_usage": device_usage,
            "content_popularity": content_popularity,
            "geographic_distribution": geographic_distribution,
        }
    )

    log.info("Transformed data with insights: " + json.dumps(data))
    return data
