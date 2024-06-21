import json


def handler(data, log):
    log.info("Event received: " + json.dumps(data))

    # Process change data capture (CDC) events
    if data["op"] == "c":  # Create operation
        log.info(f"New product added: {data['after']['product_name']}")
        data = calculate_stock_levels(data["after"])

    return data


def calculate_stock_levels(product_data):
    # Calculate stock levels and determine if restocking is needed
    stock_threshold = 10  # Example threshold for restocking
    current_stock = product_data.get("current_stock", 0)

    if current_stock <= stock_threshold:
        product_data["stock_status"] = "low_stock"
        product_data["restock_needed"] = True
    else:
        product_data["stock_status"] = "sufficient_stock"
        product_data["restock_needed"] = False

    return product_data
