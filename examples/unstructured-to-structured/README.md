# Transform unstructured data to structured in real-time

Media companies want to extract key information from livestreamed events for subtitles, translations, and content summaries but doing this manually or with bactch processing causes delays. This project showcases how to use GlassFlow for real-time extraction, transformation, and translation of YouTube video data. The handler extracts key topics from the video transcript, generates meaningful insights, and translates the transcript into any specified language. 

### Features
1. Extract video transcript from YouTube.
2. Process the data to extract topics and other meaningful data (identifies key metrics such as the number of speakers and the total duration of the spoken content).
3. Translate the transcript into the user's preferred language (for example, from English to Spanish).
4. Return structured data and derived metrics.


## Pre-requisites

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your [Personal Access Token](https://app.glassflow.dev/profile) to authorize the Python SDK to interact with GlassFlow Cloud.
- Get your OpenAI API Key https://platform.openai.com/.