import speech_recognition as sr
from tts import speak

def listen_for_voice_input(language_code):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("🎙️ Listening...")
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
            text = r.recognize_google(audio, language=language_code)
            print(f"🗣️ You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None
        except sr.UnknownValueError:
            if language_code.startswith("fr"):
                speak("Désolé, je n'ai pas compris. Veuillez réessayer.", "fr")
            elif language_code.startswith("de"):
                speak("Entschuldigung, ich habe das nicht verstanden. Bitte versuchen Sie es erneut.", "de")
            elif language_code.startswith("ro"):
                speak("Scuze, nu am înțeles. Te rog să încerci din nou.", "ro")
            elif language_code.startswith("it"):
                speak("Scusa, non ho capito. Per favore riprova.", "it")
            else:
                speak("Sorry, I couldn't understand. Please try again.")
            return None
        except sr.RequestError:
            speak("Speech recognition service unavailable.")
            return None
