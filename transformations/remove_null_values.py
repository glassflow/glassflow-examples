import json

def handler(data, log):
    data = json.loads(data)
    cleaned_data = {k: v for k, v in data.items() if v is not None}
    
    return cleaned_data
