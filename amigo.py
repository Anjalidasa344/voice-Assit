
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os


# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")

# Select a female voice if available
voices = engine.getProperty("voices")
if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)


def speak(audio):
    """Convert text into speech."""
    engine.say(audio)
    engine.runAndWait()


def take_command():
    """Listen to the microphone and recognize speech."""
    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    recognizer.non_speaking_duration = 0.5

    try:
        # Use laptop microphone (device index 1)
        with sr.Microphone(device_index=1) as source:
            print("\nListening... Speak now!")

            recognizer.adjust_for_ambient_noise(
                source, duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=6
            )

        print("Recognizing...")

        query = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("You said:", query)
        return query.lower()

    except sr.WaitTimeoutError:
        print("No speech detected.")

    except sr.UnknownValueError:
        print("Sorry, I could not understand.")

    except sr.RequestError:
        print("Speech recognition service is unavailable. Check your internet.")

    except OSError as error:
        print("Microphone error:", error)

    return ""


def search_wikipedia(query):
    """Search Wikipedia and speak a short summary."""
    try:
        search_query = query.replace("wikipedia", "").strip()

        if not search_query:
            speak("Please tell me what to search.")
            return

        speak("Searching Wikipedia.")

        result = wikipedia.summary(
            search_query,
            sentences=2
        )

        print(result)

        speak("According to Wikipedia.")
        speak(result)

    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")

    except wikipedia.exceptions.PageError:
        speak("Sorry, no Wikipedia page was found.")

    except Exception:
        speak("Unable to search Wikipedia. Please check your internet connection.")


def open_website(name, url):
    """Open a website in the default browser."""
    speak("Opening " + name)
    webbrowser.open(url)


def open_drive(drive):
    """Open a local disk if it exists."""
    path = drive + ":\\"

    if os.path.exists(path):
        speak("Opening local disk " + drive)
        os.startfile(path)
    else:
        speak("That disk is not available.")


def main():
    speak("Amigo voice assistant activated.")
    speak("How can I help you?")

    while True:
        query = take_command()

        if not query:
            continue

        if "wikipedia" in query:
            search_wikipedia(query)

        elif "who are you" in query or "are you" in query:
            speak("I am Amigo, your Python voice assistant.")

        elif "open youtube" in query:
            open_website(
                "YouTube",
                "https://www.youtube.com"
            )

        elif "open google" in query:
            open_website(
                "Google",
                "https://www.google.com"
            )

        elif "open github" in query:
            open_website(
                "GitHub",
                "https://www.github.com"
            )

        elif "open stackoverflow" in query:
            open_website(
                "Stack Overflow",
                "https://stackoverflow.com"
            )

        elif "open spotify" in query or "play music" in query:
            open_website(
                "Spotify",
                "https://open.spotify.com"
            )

        elif "open whatsapp" in query:
            open_website(
                "WhatsApp Web",
                "https://web.whatsapp.com"
            )

        elif "local disk c" in query:
            open_drive("C")

        elif "local disk d" in query:
            open_drive("D")

        elif "local disk e" in query:
            open_drive("E")

        elif any(word in query for word in ["exit", "quit", "stop", "sleep"]):
            speak("Goodbye! Amigo is shutting down.")
            break

        else:
            speak("Sorry, I don't know that command yet.")


if __name__ == "__main__":
    main()
