import json

def handler(data, log):
    log.info("Echo: " + json.dumps(data))
    if 'name' in data:
        data['message'] = "Hello World, " + data['name']
    else:
        data['message'] = "Hello World"
    return data
