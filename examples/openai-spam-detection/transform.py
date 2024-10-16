import os 
import openai

def handler(data, log):
    content = data['message']
    is_spam = detect_spam_openai(content)
    if is_spam == 1:
        data['spam_detection_openai'] = "spam"
    else:
        data['spam_detection_openai'] = "not_spam"
    
    return data

def detect_spam_openai(message):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    response = openai.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "text"},
        messages=[
            {
                "role": "system",
                "content": """Your task is to act as a content moderator. Review the following message from a chat user and classify it based on the criteria below:

1 - Spam: Unsolicited promotions, advertisements, or deceptive content. Note that messages with typos or about typical topics seen in spam messages are not necessarily spam.
0 - Non-Spam: Legitimate conversations or unclear cases. 

Return only the corresponding number (1 or 0). Any additional information will result in penalties. 
Ensure your judgment is unbiased and consistent with the criteria. Think step-by-step to make an accurate classification.
"""},
            {
                "role": "user",
                "content": f"{message}"
            }
        ],
        max_tokens=1,
        temperature=0.5,
    )
    return int(response.choices[0].message.content)

