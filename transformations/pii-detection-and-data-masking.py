import re
import json


def handler(data, log):
    log.info("Event received: " + json.dumps(data))

    # Define regex patterns for PII detection
    patterns = {
        "name": r"[A-Z][a-z]* [A-Z][a-z]*",
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\d{3}-\d{3}-\d{4}",
        "ssn": r"\d{3}-\d{2}-\d{4}",
    }

    # Mask detected PII
    masked_data = data.copy()
    for key, pattern in patterns.items():
        if key in data:
            masked_data[key] = re.sub(pattern, "[MASKED]", data[key])

    log.info("Masked data: " + json.dumps(masked_data))
    return masked_data
