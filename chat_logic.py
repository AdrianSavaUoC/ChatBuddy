import json
from config import client, DEFAULT_MODEL
from tts import speak

def get_coaching_and_answer(prompt: str, subject: str, language_label: str):
    # Sélectionne la langue cible en fonction du label
    language_rules = {
        "French": "en français clair et adapté à un jeune de 12 à 16 ans",
        "German": "auf Deutsch, klar und jugendfreundlich",
        "Italian": "in italiano semplice e adatto ai ragazzi",
        "Romanian": "în română simplă și potrivită pentru tineri",
        "English": "in simple, youth-friendly English"
    }

    system_instruction = (
    "Tu es ChatBuddy, un assistant vocal cool et curieux qui parle comme un ami de 15 ans. "
    "Tu tutoies l'utilisateur et utilises un ton détendu, drôle et amical. "
    "Tu réponds TOUJOURS dans la langue suivante : " + language_label + ". "
    "Le sujet actuel est : " + subject + ". "

    "⚠️ Très IMPORTANT : Tu dois répondre STRICTEMENT en JSON, avec ce format EXACT : "
    '{"score": nombre, "tip": "texte", "answer": "texte"}. '

    "⚠️ INTERDICTION ABSOLUE d’ajouter du texte avant ou après le JSON. "
    "Ne répond JAMAIS par des phrases hors JSON. "
    "Pas d'explications, pas de phrases supplémentaires, pas de justifications, "
    "pas de répétition de la question. UNIQUEMENT le JSON."
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

        # Extraction JSON robuste
        import re, json
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            print("⚠️ Réponse non JSON : ", response_text)
            return None

    except Exception as e:
        speak(f"⚠️ Erreur API : {e}", "fr")
        return None
