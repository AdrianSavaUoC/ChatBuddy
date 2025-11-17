from tts import speak
from languages import select_language
from subjects import choose_subject
from stt import listen_for_voice_input
from chat_logic import get_coaching_and_answer

def run_coach():
    selected_language = select_language()
    
    # Get the language code (the key from LANGUAGES dict)
    from languages import LANGUAGES
    lang_code = None
    for code, info in LANGUAGES.items():
        if info == selected_language:
            lang_code = code
            break
        
    if lang_code == 'fr':
        speak(f"Salut toi! Je m'appelle Alexiana, ton guide de conversation, je parle français. De quel sujet as-tu envie de parler aujourd'hui?", lang_code)
    elif lang_code == 'de':
        speak(f"Hallo! Ich bin Alexiana, dein KI-Gesprächstrainer. Bitte wählen Sie ein Fach aus der Liste.", lang_code)
    elif lang_code == 'it':
        speak(f"Ciao! Sono Alexiana, il tuo coach di conversazione IA in italiano. Per favore, scegli un argomento dalla lista.", lang_code)   
    else:    
        speak(f"Hello! I am Alexiana, your AI Conversation Coach in {selected_language['label']}.", lang_code)
    

    while True:
        subject = choose_subject()
        if lang_code == 'fr': 
            speak(f"Super aujourd'hui, nous allons discuter du sujet: {subject}. Poses-moi n'importe quelle question, je t'écoute.", lang_code)
        elif lang_code == 'de':
            speak(f"Heute werden wir uns auf {subject} konzentrieren .", lang_code)
        elif lang_code == 'it':
            speak(f"Oggi ci concentreremo su {subject}", lang_code)
        else:
            speak(f"Today, we'll focus on {subject}.", lang_code)
        print(lang_code)

        while True:
            # speak("Ask me anything to start!", lang_code)
            user_prompt = listen_for_voice_input(selected_language["stt"])
            if not user_prompt:
                continue

            stop_words = [
                "exit", "quit", "stop", "bye", "i'm done", "finished", "thank you",
                "sortir", "quitter", "arrêter", "au revoir", "j'ai terminé", "fini", "merci",
                "beenden", "verlassen", "stopp", "tschüss", "ich bin fertig", "fertig", "danke",
                "uscita", "esci", "ferma", "ciao", "ho finito", "finito", "grazie",
                # ❗ Je retire "pa" de la liste
                "ieșire", "ieși", "oprește", "am terminat", "terminat", "mulțumesc",
            ]

            words = user_prompt.lower().split()
            if any(word in words for word in stop_words):
                if lang_code == 'fr':
                    speak("Au revoir ! Continuez à poser de bonnes questions!", lang_code)
                elif lang_code == 'de':
                    speak(f"Auf Wiedersehen! Stell weiterhin großartige Fragen!", lang_code)
                elif lang_code == 'it':
                    speak(f"Arrivederci! Continua a fare ottime domande!", lang_code)
                else:    
                    speak("Goodbye! Keep asking great questions!", lang_code)
                break

            print("Thinking about your question...")
            coach_data = get_coaching_and_answer(user_prompt, subject, selected_language["label"])

            if coach_data:
                answer = coach_data.get("answer", "").strip()
                tip = coach_data.get("tip", "").strip()
                spoken_text = ""
                if answer:
                    spoken_text += answer + " "
                if tip:
                    spoken_text += tip
                spoken_text = spoken_text.strip()
                if spoken_text:
                    speak(spoken_text, lang_code)



if __name__ == "__main__":
    run_coach()