import speech_recognition as sr
from tts import speak
import time

def listen_for_voice_input(language_code):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        # Calibration ultra-courte (quasi instantanée)
        r.adjust_for_ambient_noise(source, duration=0.05)

        print("🎙️ Listening...")

        try:
            # Écoute hyper réactive
            audio = r.listen(
                source,
                timeout=3,            # Avant : 10 ➜ Enorme gain de fluidité
                phrase_time_limit=4   # Avant : 15 ➜ plus naturel, bonne dynamique
            )

            text = r.recognize_google(audio, language=language_code)
            print(f"🗣️ You said: {text}")
            return text

        except sr.WaitTimeoutError:
            print("⏳ Aucun son détecté.")
            return None

        except sr.UnknownValueError:
            speak("Désolé, je n'ai pas compris. Essaie encore.", "fr")
            time.sleep(0.1)
            return None

        except sr.RequestError:
            speak("La reconnaissance vocale est momentanément indisponible.")
            return None
