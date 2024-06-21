import json

def handler(data, log):
    """
    This function processes ticket data, categorizes the ticket based on its description,
    and enriches the ticket data with the identified category. Output event can be sent to vector databases.

    Args:
        data (dict): The input ticket data containing at least 'ticket_description'.
        log (object): Logger object for logging information.

    Returns:
        dict: The enriched ticket data with an additional 'category' field.
    """
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
