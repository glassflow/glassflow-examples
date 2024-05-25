import openai
import json

openai.api_key = "sk-proj-kp6FXCApPzJf1rH3wiJkT3BlbkFJQu0BrJMNzUs3ELlJgDJl"


def handler(data, log):
    """
    Generate AI insights to predict car price data.
    """
    # log.info("Event:" + json.dumps(data), data=data)

    insights = predict_price(data)
    return json.loads(insights)


def predict_price(data):
    # Generate insights using OpenAI's chat completion endpoint
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a great data analyst to predict car data prices.",
            },
            {
                "role": "user",
                "content": f"Analyze the following vehicle data: {data}, predict its price and return only the orginal full JSON with additional suggested_price attribute and value added",
            },
        ],
        max_tokens=500,
        temperature=0.5,
    )

    insights = response.choices[0].message.content
    return insights
