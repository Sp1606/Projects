# YouTube Video Summarizer
# -*- coding: utf-8 -*-

import os
import speech_recognition as sr
from pydub import AudioSegment
from transformers import pipeline
import yt_dlp

def download_video(url, save_path='./'):
    """Download YouTube video and return the file path"""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Extracting video info...")
            info_dict = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info_dict)
            print(f"Video downloaded to {video_path}")
            return video_path
    except yt_dlp.utils.DownloadError as e:
        print(f"Failed to download video: {e}")
        return None

def transcribe_audio(video_path):
    """Convert video to audio and transcribe to text"""
    if video_path is None:
        return "No video to transcribe."
    
    try:
        # Create temp directory if it doesn't exist
        os.makedirs('temp', exist_ok=True)
        audio_path = os.path.join('temp', 'lecture_audio.wav')
        
        print("Converting video to audio...")
        video = AudioSegment.from_file(video_path)
        video.export(audio_path, format="wav")

        print("Transcribing audio...")
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        
        try:
            text = recognizer.recognize_google(audio)
            print("Audio transcription complete.")
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError as e:
            return f"Error with speech recognition service: {e}"
    except Exception as e:
        return f"Error during audio transcription: {e}"
    finally:
        # Clean up temporary files
        if os.path.exists(audio_path):
            os.remove(audio_path)

def summarize_text(text):
    """Generate summary of transcribed text"""
    try:
        print("Loading summarization model...")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        print("Summarizing text...")
        
        # Split long text into chunks (Google Speech-to-Text has limits)
        max_chunk_size = 1000  # characters
        chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
        
        summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        
        return " ".join(summaries)
    except Exception as e:
        return f"Error during text summarization: {e}"

def summarize_youtube_lecture(url):
    """Main function to process YouTube URL"""
    print("\n=== YouTube Video Summarizer ===")
    print("Downloading video...")
    video_path = download_video(url)
    
    if video_path is None:
        return "Video download failed. Cannot proceed."

    print("\nProcessing audio transcription...")
    text = transcribe_audio(video_path)
    
    if text.startswith(("Error", "Could not", "No video")):
        return text

    print("\nGenerating summary...")
    summary = summarize_text(text)
    
    # Clean up downloaded video
    if os.path.exists(video_path):
        os.remove(video_path)
    
    return summary

if __name__ == "__main__":
    # Install required packages (uncomment if needed)
    # import subprocess
    # subprocess.run(['pip', 'install', 'pytube', 'SpeechRecognition', 'pydub', 'transformers', 'yt-dlp'])
    
    # Example usage
    url = "https://www.youtube.com/watch?v=FrNqSLPaZLc"  # Replace with your video URL
    summary = summarize_youtube_lecture(url)
    
    print("\n=== Final Summary ===")
    print(summary)