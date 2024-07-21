import json


def handler(data, log):
    log.info("Event received: " + json.dumps(data))

    # Check for required fields
    required_fields = ["text", "user_id"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        data["quality_check"] = f"Missing fields: {', '.join(missing_fields)}"
        data["is_valid"] = False
    else:
        text = data["text"].strip()
        if len(text) < 5:
            data["quality_check"] = "Text too short"
            data["is_valid"] = False
        else:
            data["quality_check"] = "All checks passed"
            data["is_valid"] = True

    return data
