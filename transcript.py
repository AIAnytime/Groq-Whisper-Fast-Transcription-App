import streamlit as st
import os
import base64
import yt_dlp
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()

# Initialize OpenAI client for Groq API
groq = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# Function to convert audio file to base64
def audio_to_base64(file):
    with open(file, "rb") as audio_file:
        audio_bytes = audio_file.read()
        base64_audio = base64.b64encode(audio_bytes).decode()
    return base64_audio

# Function to re-encode audio file to opus (ogg) format
def reencode_audio_to_ogg(input_file, output_file="encoded_audio.ogg"):
    command = [
        "ffmpeg", "-y",  # Add the '-y' flag to overwrite without asking
        "-i", input_file, "-vn", "-map_metadata", "-1", 
        "-ac", "1", "-c:a", "libopus", "-b:a", "12k", "-application", "voip", output_file
    ]
    subprocess.run(command, check=True)

# Function to download YouTube video and convert to audio (MP3)
def download_youtube_audio(youtube_url, output_file="youtube_audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': "%(title)s.%(ext)s",  # Use title for the name and mp3 as the extension
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url)
        downloaded_filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    
    if os.path.exists(output_file):
        os.remove(output_file)
    
    os.rename(downloaded_filename, output_file)

# Streamlit App Setup
st.set_page_config(layout="wide", page_title="🎤 Groq Whisper Fast Transcription")

# Add custom CSS to improve UI styling
st.markdown("""
    <style>
    .main {
        
        padding: 10px;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stButton button {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🎙️ Groq Whisper Transcription App")

# Tabs for File Upload and YouTube Link
tab1, tab2 = st.tabs(["📂 Upload Audio", "🎥 YouTube to Audio"])

# Tab 1: Upload Audio and Transcription
with tab1:
    st.header("🎧 Upload MP3 for Transcription")
    st.write("Upload your MP3 file and get a transcription in a few seconds.")

    uploaded_file = st.file_uploader("🔊 Upload an MP3 file", type=["mp3"])
    
    if uploaded_file is not None:
        with st.spinner("⚙️ Processing your audio..."):
            # Save the uploaded file to disk
            with open("uploaded_file.mp3", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Re-encode the uploaded audio to OGG (Opus) format to reduce file size
            reencode_audio_to_ogg("uploaded_file.mp3", "encoded_audio.ogg")

            # Convert the re-encoded OGG file to base64 for embedding in HTML
            base64_audio = audio_to_base64("encoded_audio.ogg")

            # Embed the audio file in HTML
            audio_html = f"""
            <audio controls>
                <source src="data:audio/ogg;base64,{base64_audio}" type="audio/ogg">
                Your browser does not support the audio element.
            </audio>
            """
            st.subheader("🎶 Your Uploaded and Re-encoded Audio File")
            st.markdown(audio_html, unsafe_allow_html=True)
            st.success("✅ Audio processing complete!")
    
    if st.button("📝 Transcribe"):
        with st.spinner("⏳ Transcribing your audio..."):
            with open("encoded_audio.ogg", "rb") as audio_file:
                transcript = groq.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=audio_file,
                    response_format="text"
                )
        st.success("🎉 Transcription: " + transcript)

# Tab 2: YouTube Link to Audio and Transcription
with tab2:
    st.header("🎥 Transcribe YouTube Video Audio")
    st.write("Enter a YouTube URL to download and transcribe the audio.")

    youtube_url = st.text_input("🔗 Enter YouTube Video URL")

    if st.button("⬇️ Download and Transcribe"):
        if youtube_url:
            with st.spinner("⚙️ Downloading and processing audio..."):
                # Download YouTube video and extract audio
                download_youtube_audio(youtube_url, "youtube_audio.mp3")

                # Re-encode the downloaded audio to OGG (Opus) format
                reencode_audio_to_ogg("youtube_audio.mp3", "encoded_youtube_audio.ogg")

                # Convert the re-encoded OGG file to base64 for embedding in HTML
                base64_audio = audio_to_base64("encoded_youtube_audio.ogg")

                # Embed the audio file in HTML
                audio_html = f"""
                <audio controls>
                    <source src="data:audio/ogg;base64,{base64_audio}" type="audio/ogg">
                    Your browser does not support the audio element.
                </audio>
                """
                st.subheader("🎶 Downloaded and Re-encoded YouTube Audio")
                st.markdown(audio_html, unsafe_allow_html=True)

            with st.spinner("⏳ Transcribing YouTube audio..."):
                with open("encoded_youtube_audio.ogg", "rb") as audio_file:
                    transcript = groq.audio.transcriptions.create(
                        model="whisper-large-v3",
                        file=audio_file,
                        response_format="text"
                    )
            st.success("🎉 Transcription: " + transcript)
        else:
            st.error("❌ Please enter a valid YouTube URL")
