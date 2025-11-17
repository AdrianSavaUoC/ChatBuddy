import os
import platform
import subprocess
import tempfile
import soundfile as sf
import sounddevice as sd

# OS detection
system = platform.system()
PIPER_BINARY = "piper.exe" if system == "Windows" else "piper"
PIPER_PATH = os.path.join("piper", PIPER_BINARY)

# Model paths
MODEL_PATHS = {
    "fr": "piper/models/fr_FR-siwis-medium.onnx",
}

# Track if Piper was announced once
PIPER_LOADED_ONCE = False


def speak(text, lang_code="fr"):
    global PIPER_LOADED_ONCE

    # PRINT FOR DEBUG
    print(f"🎙️ ChatBuddy: {text}")

    # 🔥 Fix: skip empty text
    if not text or text.strip() == "":
        return

    model_path = MODEL_PATHS.get(lang_code, MODEL_PATHS["fr"])

    # Temporary WAV output file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        wav_path = tmp.name

    try:
        # Run Piper silently with expressive params
        process = subprocess.Popen(
            [
                PIPER_PATH,
                "--model", model_path,
                "--output_file", wav_path,
                "--noise_scale", "0.5",
                "--noise_w", "0.8",
                "--length_scale", "0.9",
                "--sentence_silence", "0.2"
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        process.communicate(input=text.encode("utf-8"))

        # Announce Piper startup only once
        if not PIPER_LOADED_ONCE:
            print("🔊 Piper TTS prêt !")
            PIPER_LOADED_ONCE = True

        # Check if WAV is valid
        if not os.path.exists(wav_path) or os.path.getsize(wav_path) < 200:
            print("⚠️ Piper n’a pas généré de son. Vérifie ton modèle ou ton texte.")
            return

        # Read WAV properly
        audio, sr = sf.read(wav_path, dtype="float32")

        # Play
        sd.play(audio, sr)
        sd.wait()

    except Exception as e:
        print(f"⚠️ Piper TTS error: {e}")

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)
