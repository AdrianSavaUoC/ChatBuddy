import pyttsx3

tts_engine = None
DEFAULT_VOICE_ID = None
LANGUAGE_VOICES = {}

def init_tts():
    """Initialise le moteur TTS et détecte les voix locales."""
    global DEFAULT_VOICE_ID, LANGUAGE_VOICES
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        if voices:
            DEFAULT_VOICE_ID = voices[0].id
            for voice in voices:
                voice_id_lower = voice.id.lower()
                voice_name_lower = voice.name.lower() if hasattr(voice, 'name') else ""

                if 'en' in voice_id_lower or 'english' in voice_name_lower:
                    LANGUAGE_VOICES.setdefault('en', voice.id)
                if 'fr' in voice_id_lower or 'french' in voice_name_lower or 'français' in voice_name_lower:
                    LANGUAGE_VOICES.setdefault('fr', voice.id)
                if 'de' in voice_id_lower or 'german' in voice_name_lower or 'deutsch' in voice_name_lower:
                    LANGUAGE_VOICES.setdefault('de', voice.id)
                if 'it' in voice_id_lower or 'italian' in voice_name_lower or 'italiano' in voice_name_lower:
                    LANGUAGE_VOICES.setdefault('it', voice.id)
                if 'ro' in voice_id_lower or 'romanian' in voice_name_lower:
                    LANGUAGE_VOICES.setdefault('ro', voice.id)

            print(f"✅ Voix disponibles : {list(LANGUAGE_VOICES.keys())}")

        engine.stop()
    except Exception as e:
        print(f"⚠️ Erreur d’initialisation TTS : {e}")
        DEFAULT_VOICE_ID = None


def get_voice_for_language(lang_code):
    """Renvoie l’ID de la voix pour la langue donnée."""
    return LANGUAGE_VOICES.get(lang_code, DEFAULT_VOICE_ID)


def speak(text, lang_code="fr"):
    """Parle le texte en utilisant pyttsx3 (offline, stable)."""
    print(f"🎙️ ChatBuddy: {text}")

    global tts_engine
    try:
        tts_engine = pyttsx3.init()
        tts_engine.setProperty("rate", 175)
        tts_engine.setProperty("volume", 1.0)

        voice_to_use = get_voice_for_language(lang_code)
        if voice_to_use:
            tts_engine.setProperty("voice", voice_to_use)

        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"⚠️ Erreur TTS : {e}")
    finally:
        if tts_engine:
            tts_engine.stop()
            tts_engine = None
