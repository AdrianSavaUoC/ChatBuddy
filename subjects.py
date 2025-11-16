from tts import speak

SUBJECTS = [
    "Science",
    "Mathématiques",
    "Histoire",
    "Géographie",
    "Art",
    "Musique",
    "Technologie",
    "Sport",
    "Littérature"
]

def choose_subject():
    print("\n📚 Available subjects:")
    for i, subj in enumerate(SUBJECTS, 0):
        print(f"{i}. {subj}")

    # speak("Please choose a subject from the list.")

    while True:
        choice = input("Choose a subject by number (1–9): ").strip()
        if choice.isdigit() and 0 <= int(choice) <= len(SUBJECTS):
            selected = SUBJECTS[int(choice)]
            # speak(f"You chose {selected}. Great choice!")
            return selected
        else:
            speak("Invalid choice. Try again.")
