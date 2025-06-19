import speech_recognition as sr
import pyttsx3

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print("🗣️ You said:", query)
            return query
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "API unavailable."

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()