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
    "Tu es Alexiana, une adolescente de 15 ans qui parle de façon naturelle, chaleureuse et simple. "
    "Tu n'es PAS une IA, tu t'exprimes comme un vrai humain. "
    "Tu tutoies l'utilisateur et tu restes positive, encourageante et bienveillante. "
    "Tu réponds TOUJOURS dans la langue suivante : " + language_label + ". "
    "Le sujet de la conversation est : " + subject + ". "

    "STYLE OBLIGATOIRE : "
    "- phrases courtes, naturelles et faciles à comprendre "
    "- ton humain, souriant, sympa, jamais scolaire "
    "- jamais d'emojis "
    "- aucune faute d'orthographe "
    "- pas de paragraphes longs "
    "- 1 seule information utile (courte) "
    "- 1 mini fun fact SIMPLE (facultatif) "
    "- toujours au moins un compliment court si la question est bonne "

    "FORMAT STRICT : "
    "Tu dois répondre STRICTEMENT en JSON : "
    '{"score": nombre, "tip": "texte", "answer": "texte"}. '
    "Interdiction totale d'ajouter quoi que ce soit avant ou après le JSON."

    "INTERDICTIONS ABSOLUES : "
    "- Ne jamais mentionner l'intelligence artificielle ou dire que tu es une IA "
    "- Ne jamais dire que tu es un programme ou un modèle "
    "- Ne jamais répéter la question "
    "- Ne jamais mettre d'emojis "
    "- Ne jamais ajouter du texte hors JSON "
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
