print("starting...")

import os
import json
import speech_recognition as sr
import pyttsx3
from openai import OpenAI


# --- 1. CONFIGURATION AND INITIALIZATION (Infomaniak API Setup) ---

# 🟢 SECURITY FIX: Reading credentials from environmental variables
OPENAI_API_KEY = os.getenv("INFOMANIAK_API_TOKEN")
PRODUCT_ID = os.getenv("INFOMANIAK_PRODUCT_ID")

if not OPENAI_API_KEY:
    print("FATAL ERROR: The INFOMANIAK_API_TOKEN environment variable is missing.")
    exit()

if not PRODUCT_ID:
    print("FATAL ERROR: The INFOMANIAK_PRODUCT_ID environment variable is missing.")
    exit()

# Base URL construction remains the same
INFOMANIAK_BASE_URL = f"https://api.infomaniak.com/1/ai/{PRODUCT_ID}/openai"
print(f"🔗 Using Infomaniak API endpoint: {INFOMANIAK_BASE_URL}")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY, base_url=INFOMANIAK_BASE_URL)

# --- Language setup ---
LANGUAGES = {
    "en": {"label": "English", "stt": "en-US"},
    "fr": {"label": "French", "stt": "fr-FR"},
    "de": {"label": "German", "stt": "de-DE"},
    "it": {"label": "Italian", "stt": "it-IT"},
    "ro": {"label": "Romanian", "stt": "ro-RO"},
}

print("🌍 Available languages:")
for code, info in LANGUAGES.items():
    print(f"  {code}: {info['label']}")

lang_choice = input("Select your language (en/fr/de/it/ro): ").strip().lower()
if lang_choice not in LANGUAGES:
    print("Invalid choice. Defaulting to English.")
    lang_choice = "en"

selected_language = LANGUAGES[lang_choice]
print(f"✅ Language set to {selected_language['label']}.")


# --- Text To Speech setup ---
tts_engine = None
try:
    tts_engine_check = pyttsx3.init()
    voices = tts_engine_check.getProperty('voices')
    if voices:
        print(f"✅ TTS Engine initialised successfully with voice: {voices[0].name}")
        SELECTED_VOICE_ID = voices[0].id
    else:
        print("⚠️ No voices found. Speech will not work.")
        SELECTED_VOICE_ID = None
    tts_engine_check.stop()
    tts_engine_check = None
except Exception as e:
    print(f"❌ TTS initialisation failed: {e}")
    SELECTED_VOICE_ID = None


def speak(text):
    """Speaks text, re-initializing the engine each time."""
    global tts_engine
    print(f"🎙️ Coach: {text}")

    if SELECTED_VOICE_ID is None:
        return

    tts_engine = None
    try:
        tts_engine = pyttsx3.init()
        tts_engine.setProperty("rate", 150)
        tts_engine.setProperty('voice', SELECTED_VOICE_ID)
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"❌ Speak failed: {e}")
    finally:
        if tts_engine:
            try:
                tts_engine.stop()
            except:
                pass
            tts_engine = None


# --- Subject selection ---
SUBJECTS = [
    "Science",
    "Mathematics",
    "History",
    "Geography",
    "Art",
    "Music",
    "Technology",
    "Sports",
    "Literature"
]

def choose_subject():
    print("\n📚 Available subjects:")
    for i, subj in enumerate(SUBJECTS, 1):
        print(f"{i}. {subj}")
    speak("Please choose a subject from the list.")
    # for subj in SUBJECTS:
    #     speak(subj)

    while True:
        choice = input("\nChoose a subject by number (1–9): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(SUBJECTS):
            selected = SUBJECTS[int(choice) - 1]
            speak(f"You chose {selected}. Great choice!")
            return selected
        else:
            speak("Invalid choice. Try again.")


# --- Speech-to-text ---
def listen_for_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("🎙️ Listening...")

        try:
            audio = r.listen(source, timeout=5) # phrase_time_limit=10
            text = r.recognize_google(audio, language=selected_language["stt"])
            print(f"🗣️ You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Please try again.")
            return None
        except sr.RequestError:
            speak("Speech recognition service unavailable.")
            return None


# --- Chat logic ---
VALID_MODELS = [
    'mixtral', 'mixtral8x22b', 'llama3', 'granite', 'reasoning',
    'mistral24b', 'mistral3', 'qwen3', 'gemma3n', 'Qwen/Qwen3-Coder-480B-A35B-Instruct'
]
DEFAULT_MODEL = VALID_MODELS[0]

def get_coaching_and_answer(prompt: str, subject: str):
    system_instruction = (
        f"You are ChatBuddy, an AI Conversation Coach for young people aged 12–16. "
        f"Focus all responses on the topic of {subject}. "
        f"Respond entirely in {selected_language['label']}. "
        "Your goal is to teach them how to communicate well with AI. "
        "1. Analyse their prompt for clarity, specificity, and context, scoring it out of 100. "
        "2. Provide one short, friendly, actionable coaching tip. "
        "3. Provide a funny, helpful, age-appropriate answer about the chosen subject. "
        "4. Always include a small fun fact or joke related to the topic. "
        "5. Never provide medical, legal, or harmful advice. "
        "Respond strictly as valid JSON with keys: "
        "{'score': integer, 'tip': string, 'answer': string}."
    )
    try:
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
        )
        response_text = completion.choices[0].message.content.strip()
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        json_str = response_text[start:end]
        return json.loads(json_str)
    except Exception as e:
        speak(f"⚠️ API error: {e}")
        return None


# --- Main loop ---
def run_coach():
    
    speak(f"Hello! I am ChatBuddy, your AI Conversation Coach in {selected_language['label']}.")

    subject = choose_subject()
    speak(f"Today, we’ll focus on {subject}.")

    while True:
        speak("Ask me anything to start!")
        user_prompt = listen_for_voice_input()
        if not user_prompt:
            continue

        stop_words = ["exit", "quit", "stop", "bye", "i'm done" ,"finished", "thank you"]
        if any(word in user_prompt.lower() for word in stop_words):
            speak("Goodbye! Keep asking great questions!")
            # break 
            subject = choose_subject()
            coach_data = get_coaching_and_answer(user_prompt, subject)

            
        else:         
            print("Thinking about your question...")
            coach_data = get_coaching_and_answer(user_prompt, subject)
    
            if coach_data:
                score = coach_data.get("score", 0)
                tip = coach_data.get("tip", "No tip this time.")
                answer = coach_data.get("answer", "No answer generated.")
    
                speak(answer)
                # speak(f"I rated your question {score} out of 100 for clarity.")
                speak(f"Quick Tip: {tip}")


if __name__ == "__main__":
    run_coach()







