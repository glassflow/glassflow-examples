import json


def handler(data, log):
    log.info("Event received: " + json.dumps(data))

    # Keywords for categorizing tickets
    categories = {
        "network": ["internet", "wifi", "network"],
        "hardware": ["printer", "computer", "keyboard"],
        "software": ["software", "application", "program"],
    }

    # Function to categorize ticket
    def categorize_ticket(description):
        for category, keywords in categories.items():
            if any(keyword in description.lower() for keyword in keywords):
                return category
        return "other"

    # Enrich ticket data with category
    data["category"] = categorize_ticket(data["ticket_description"])
    return data
