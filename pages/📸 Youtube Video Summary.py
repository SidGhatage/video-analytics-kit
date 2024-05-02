import streamlit as st
from dotenv import load_dotenv
from textblob import TextBlob

load_dotenv() ##load all the environment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here. Also if you find any mathematical term or definition or theorem, then provide its mathematical expression or formula:  """

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        st.error(f"Error extracting transcript: {e}")

## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(input_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt+input_text)
        return response.text

    except Exception as e:
        st.error(f"Error generating summary: {e}")

def extract_keywords(input_text):
    try:
        prompt = "Extract important keywords from the text:\n"
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + input_text)
        keywords = response.text.split(", ")
        return keywords

    except Exception as e:
        st.error(f"Error extracting keywords: {e}")

def get_references(input_text):
    try:
        prompt = "Provide other references or suggestions related to the input video:\n"
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + input_text)
        references = response.text.split("\n")
        return references

    except Exception as e:
        st.error(f"Error generating references: {e}")

def get_sentiment_label(polarity):
    if polarity > 0:
        return "Positive"
    elif polarity == 0:
        return "Neutral"
    else:
        return "Negative"

st.title("YouTube Transcript to Detailed Notes Converter")

# Input field for YouTube video link
youtube_link = st.text_input("Enter YouTube Video Link:")

# Input field for text input
input_text = st.text_area("Input Text")

# If YouTube link is provided, display the video thumbnail
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# If input text is provided and the button is clicked, generate summary, sentiment analysis, and extract keywords
if st.button("Get Detailed Notes"):
    if youtube_link:
        transcript_text = extract_transcript_details(youtube_link)
    elif input_text:
        transcript_text = input_text.strip()

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)

        # Perform sentiment analysis
        blob = TextBlob(transcript_text)
        sentiment = blob.sentiment

        # Determine sentiment label
        sentiment_label = get_sentiment_label(sentiment.polarity)

        # Display sentiment analysis results
        st.markdown("## Sentiment Analysis:")
        st.write(f"Polarity: {sentiment.polarity}")
        st.write(f"Subjectivity: {sentiment.subjectivity}")
        st.write(f"Sentiment: {sentiment_label}")

        # Extract keywords
        keywords = extract_keywords(transcript_text)
        st.markdown("## Extracted Keywords:")
        if keywords:
            st.write(", ".join(keywords))
        else:
            st.write("No keywords extracted.")

        # Get references
        references = get_references(transcript_text)
        st.markdown("## References and Suggestions:")
        if references:
            for ref in references:
                st.write(ref)
        else:
            st.write("No references or suggestions generated.")
