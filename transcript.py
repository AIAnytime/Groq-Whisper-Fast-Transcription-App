import streamlit as st
import os
import base64
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
groq = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

llm = AzureChatOpenAI(openai_api_version=OPENAI_API_GPT_4_VERSION,
                    azure_deployment=DEPLOYMENT_NAME_GPT_4o,
                    model="gpt-4o",
                    temperature=0.7,
                    openai_api_key=OPENAI_API_GPT_4_KEY,
                    azure_endpoint=OPENAI_API_GPT_4_BASE
)

# Function to convert audio file to base64
def audio_to_base64(file):
    audio_file = open(file, "rb")
    audio_bytes = audio_file.read()
    base64_audio = base64.b64encode(audio_bytes).decode()
    return base64_audio

st.set_page_config(
    layout="wide",
    page_title = "AI App"
)

st.title("Flight Incident Investigation Report App")

uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])



if uploaded_file is not None:
# Save the uploaded file to disk
with open("uploaded_file.mp3", "wb") as f:
f.write(uploaded_file.getbuffer())

# Convert the uploaded MP3 file to base64 for embedding in HTML
base64_audio = audio_to_base64("uploaded_file.mp3")

# Embed the audio file in HTML
audio_html = f"""
<audio controls>
    <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3">
    Your browser does not support the audio element.
</audio>
"""
st.subheader("Your Uploaded Audio File")
st.markdown(audio_html, unsafe_allow_html=True)

if st.button("Analyze"):

# Transcribe the audio using OpenAI API
with open("uploaded_file.mp3", "rb") as audio_file:
    transcript = groq.audio.transcriptions.create(
        model="whisper-large-v3",
        file=audio_file,
        response_format="text"
    )

st.success("Raw Transcription: "+transcript)

