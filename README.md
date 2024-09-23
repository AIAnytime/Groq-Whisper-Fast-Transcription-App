
# Groq Whisper AI Fast Transcription App
![Screenshot 2024-09-23 161319](https://github.com/user-attachments/assets/2d8562ab-4302-4856-8900-042cdd677ae6)

![Screenshot 2024-09-23 161338](https://github.com/user-attachments/assets/7ac5a5e0-c3ec-4154-8e59-84eae60bf52a)





This Streamlit-based app allows users to transcribe audio files or YouTube videos using Groq Whisper API. It provides two main functionalities:
1. Upload an MP3 file for transcription.
2. Input a YouTube URL, download the audio, and transcribe it.

## Features

- **Audio Upload**: Upload any MP3 file, re-encode it to OGG format to reduce file size, and transcribe it using the Groq Whisper API.
- **YouTube Audio Download**: Provide a YouTube link, download the audio, re-encode it to OGG, and get a transcription.
- **Re-encoding**: Uses `ffmpeg` to re-encode MP3 files to the Opus codec in OGG format, ensuring compatibility with Whisper's input limits (maximum 25MB).
- **Audio Embedding**: After re-encoding, the audio file is embedded in the Streamlit app with a player for users to listen to the audio directly.

## Technologies Used

- **Streamlit**: Used for building the web interface.
- **yt-dlp**: To download YouTube videos and extract audio.
- **pydub**: Audio processing library.
- **ffmpeg**: Used for re-encoding the audio into OGG format.This compresses the audio significantly while retaining quality suitable for transcription.
- **Groq Whisper API**: Used for transcribing the audio.
- **Python**: Core programming language for the app.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10 or higher
- `ffmpeg` (ensure it’s in your system's PATH)
- Necessary Python dependencies (installed using `requirements.txt`)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Vinay9911/Groq-Whisper-Fast-Transcription-App.git
   ```

2. Navigate to the project directory:

   ```bash
   cd groq-whisper-fast-transcription-app
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure `ffmpeg` is installed on your machine and available in your system's PATH.

5. Create a `.env` file in the root directory with the following contents:

   ```bash
   GROQ_API_KEY=your_groq_api_key
   ```

   Replace `your_groq_api_key` with your actual Groq Whisper API key.

## Usage

1. Run the Streamlit app:

   ```bash
   streamlit run transcript.py
   ```

2. The app will open in your default web browser. You can also access it at `http://localhost:8501`.

3. **Transcription Options**:
   - **Tab 1 - Upload Audio**: Upload an MP3 file, which will be re-encoded and then transcribed using Groq Whisper.
   - **Tab 2 - YouTube to Audio**: Enter a YouTube video URL, download the audio, and get a transcription.



## Notes

- The Groq Whisper API can transcribe long audio files, but re-encoding is necessary to reduce file size for optimal performance.
- Ensure you have a stable internet connection, as the app interacts with the Groq API for transcription.

## Project Structure

```
groq-whisper-fast-transcription-app/
│
├── .env                # Contains the Groq API key
├── transcript.py       # Main Python file for the Streamlit app
├── requirements.txt    # Python dependencies
└── README.md           # This README file
```
.
