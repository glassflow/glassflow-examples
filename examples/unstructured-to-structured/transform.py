import openai
from youtube_transcript_api import YouTubeTranscriptApi
import os

# You will need an API key from OpenAI for this to work
openai.api_key = os.getenv("OPENAI_API_KEY")


# GlassFlow mandatory handler function
def handler(data, log):
    """
    GlassFlow handler function for extracting key insights from YouTube video transcripts,
    translating the transcript into another language, and generating derived metrics.

    Parameters:
    - event: Incoming event data containing a YouTube link and target language for translation.
    - log: Logging object for GlassFlow pipeline.

    Returns:
    - A dictionary containing the translated transcript, transcript length in minutes,
      number of distinct speakers, and average words spoken per speaker.
    """
    try:
        log.info("Starting YouTube transcript processing and data extraction")

        # Validate input data
        youtube_link = data["youtube_link"]
        target_language = data["target_language"]

        if not youtube_link or not target_language:
            log.error("Missing youtube_link or target_language in the event")
            return {"error": "Missing youtube_link or target_language"}

        # Step 2: Fetch transcript from YouTube
        transcript = get_transcription_from_youtube(youtube_link)

        if not transcript:
            log.error(f"Could not retrieve transcript for video: {youtube_link}")
            return {"error": "Transcript not found"}

        # Step 3: Translate transcript to target language using OpenAI
        translated_transcript = translate_transcript(transcript, target_language)

        # Step 4: Calculate derived metrics such as transcript length and distinct speaker analysis
        derived_metrics = derive_metrics(transcript, log)

        # Build the final structured event data
        processed_event = {
            "youtube_link": youtube_link,
            "translated_transcript": translated_transcript,
            "transcript_length_minutes": derived_metrics["transcript_length_minutes"],
            "number_of_speakers": derived_metrics["number_of_speakers"],
            "average_words_per_speaker": derived_metrics["average_words_per_speaker"],
        }

        log.info(f"Processed event: {processed_event}")
        return processed_event

    except Exception as e:
        log.error(f"Error during YouTube transcript transformation: {e}")
        raise


# Step 2: Fetch YouTube Transcript


def get_transcription_from_youtube(youtube_link):
    """
    Fetches the transcript from a YouTube video using the video ID.
    """
    try:
        video_id = youtube_link.split("v=")[-1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Convert transcript (list of dicts) to a string
        transcript_text = " ".join([entry["text"] for entry in transcript_list])
        return transcript_text

    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None


# Step 3: Translate Transcript Using OpenAI


def translate_transcript(transcript, target_language):
    """
    Translate a video transcript into a target language using OpenAI GPT.

    Parameters:
    - transcript: The full transcript of the video.
    - target_language: Language to translate the transcript into.

    Returns:
    - Translated transcript in the target language.
    """
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a great to analyze YouTube videos.",
            },
            {
                "role": "user",
                "content": f"Translate the following transcript into {target_language}:\n\n{transcript}",
            },
        ],
        max_tokens=100,
        temperature=0.5,
    )

    translated_transcript = response.choices[0].message.content
    return translated_transcript


# Step 4: Calculate Derived Metrics
def derive_metrics(transcript, log):
    """
    Derive meaningful metrics from the transcript, such as transcript length (in minutes),
    number of distinct speakers, and average words per speaker.

    Parameters:
    - transcript: The full transcript of the video.

    Returns:
    - Dictionary containing derived metrics such as transcript length, number of speakers,
      and average words spoken per speaker.
    """
    log.info("Calculating derived metrics from the transcript")

    # Calculate transcript length (assuming 3 words per second)
    word_count = len(transcript.split())
    transcript_length_minutes = word_count / (3 * 60)  # 3 words per second

    # Simulate the identification of distinct speakers (For simplicity, we'll assume we have 3 speakers)
    number_of_speakers = (
        3  # You can use advanced models to identify speakers from transcript
    )

    # Calculate average words spoken per speaker
    average_words_per_speaker = word_count / number_of_speakers

    derived_metrics = {
        "transcript_length_minutes": round(transcript_length_minutes, 2),
        "number_of_speakers": number_of_speakers,
        "average_words_per_speaker": round(average_words_per_speaker, 2),
    }

    return derived_metrics
