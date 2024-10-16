from llama_index.core.postprocessor import NERPIINodePostprocessor
import os 


def ner(mytext):
    HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
    import requests
    API_URL = "https://api-inference.huggingface.co/models/dbmdz/bert-large-cased-finetuned-conll03-english"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": mytext
    })
    if 'error' in output:
        raise Exception("Error in getting response from hugging face. Error: %s" % output['error'])
    return output


def handler(data, log):
    text_field = data['text']
    processor = NERPIINodePostprocessor()
    resp = processor.mask_pii(ner, text_field)
    data['text_masked'] = resp[0]
    data['entities'] = resp[1]
    return data


