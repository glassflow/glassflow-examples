import openai
import json

openai.api_key = "{REPLACE_WITH_YOUR_OPENAI_API_KEY}"


def handler(data, log):
    """
    Generate AI insights, detect anomalies and transform server logs data.
    """
    log.info("Event:" + json.dumps(data), data=data)

    insights = detect_anomalies(data)
    return {
        "text": f"Status: {'suspicious' if 'suspicious' in insights else 'unusual'}\nDetails: {insights}"
    }


def detect_anomalies(log):
    # Generate insights using OpenAI's chat completion endpoint
    response = openai.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a great data analyst to detect anomalies on server logs.",
            },
            {
                "role": "user",
                "content": f"Analyze the following log: {log}, identify if it is unusual or suspicious and return only unusual or suspicious in the JSON with status attribute and log itself as a second variable",
            },
        ],
        max_tokens=150,
        temperature=0.5,
    )

    insights = response.choices[0].message.content
    return insights
