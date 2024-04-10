# transform.py
import json

# Write a mandatory 'handler' function
def handler(data, log):
    log.info("Event:" + json.dumps(data), data=data)
    # Example transformation: Convert units from pounds to kilograms
    if data['unit'] == 'pounds':
        pound_quantity = data['quantity']
        data['quantity'] = float(pound_quantity) * 0.453592       
        data['unit'] = 'kg'
    
    return data