ChatBuddy – AI Voice Conversation Coach

ChatBuddy is an AI-powered voice assistant designed to help young learners (ages 12–16) improve their communication and learning skills. It uses OpenAI via Infomaniak API for generating age-appropriate coaching, tips, and answers, and allows voice interactions with real-time speech-to-text and text-to-speech.

# ChatBuddy – AI Voice Assistant

ChatBuddy is a Python-based AI voice assistant designed to help young people (12–16 years old) practice asking clear, specific questions and receive friendly, age-appropriate coaching. The assistant uses **speech recognition**, **text-to-speech**, and an **OpenAI-compatible API** (via Infomaniak) to interact with the user.

---

## Features

- **Voice Interaction**: Speak your questions to ChatBuddy and receive spoken responses.  
- **AI Coaching**: Questions are analyzed for clarity, and ChatBuddy provides actionable tips.  
- **Age-Appropriate Answers**: Responses are friendly, safe, and suitable for teens.  
- **Fun Extras**: Answers may include jokes or interesting facts related to your question.  
- **Stop Commands**: Easily exit the session by saying “exit”, “quit”, “bye”, or similar.

---

## Requirements

- Python 3.10+
- Libraries:
  - `speechrecognition`
  - `pyttsx3`
  - `openai` (official Python SDK)
- Microphone and speakers/headphones for voice input/output.

You can install the required libraries using:
'pip install speechrecognition pyttsx3 openai'

Project Structure

ChatBuddy/
├── main.py             # Main Python script with voice assistant logic
├── .project            # Eclipse project metadata
├── .pydevproject       # Eclipse Python settings
├── .settings/          # Eclipse workspace settings
└── README.md           # This file

Notes & Recommendations

Pyttsx3 voice output may sound unnatural depending on your system’s available voices.

Longer questions are supported, and ChatBuddy waits for the user to finish speaking.

Keep your API keys secure! Avoid committing real tokens to public repositories.


