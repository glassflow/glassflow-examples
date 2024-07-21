import openai
import json


def handler(data, log):
    log.info("Event:" + json.dumps(data), data=data)

    insights = detect_anomalies(data)
    return json.loads(insights)


def detect_anomalies(log):
    openai.api_key = "{REPLACE_WITH_YOUR_OPENAI_API_KEY}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a great data analyst to detect anomalies on server logs.",
            },
            {
                "role": "user",
                "content": f"Analyze the following log: {log}, identify if it is normal, unusual or suspicious",
            },
        ],
        max_tokens=100,
        temperature=0.5,
    )

    insights = response.choices[0].message.content
    return insights
