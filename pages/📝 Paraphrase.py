import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a text paraphraser. Please paraphrase the following text:\n\n"""

st.title("Text Paraphraser")

# Input field for text input
input_text = st.text_area("Input Text")

# If input text is provided and the button is clicked, generate paraphrased text
if st.button("Paraphrase Text"):
    if input_text:
        # Initialize the GenerativeModel for paraphrasing
        model = genai.GenerativeModel("gemini-pro")

        # Generate paraphrased text using the Google Generative AI API
        paraphrased_text = model.generate_content(prompt + input_text).text

        st.markdown("## Paraphrased Text:")
        st.write(paraphrased_text)
