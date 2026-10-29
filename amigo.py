
import datetime
import random
import webbrowser
import speech_recognition as sr
import pyttsx3
import wikipedia
from ddgs import DDGS

# -------------------------------
# AMIGO VOICE ASSISTANT - VERSION 3.2
# -------------------------------

# Text-to-speech setup
engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

try:
    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)
except Exception as error:
    print("Voice setup error:", error)


# -------------------------------
# SPEAK FUNCTION
# -------------------------------

def speak(text):
    import subprocess, sys
    message = str(text).strip()
    if not message:
        return
    print("Amigo:", message)
    voice_code = 'import sys, pyttsx3; e=pyttsx3.init("sapi5"); e.setProperty("volume", 1.0); e.setProperty("rate", 150); e.say(sys.argv[1]); e.runAndWait(); e.stop()'
    try:
        subprocess.run([sys.executable, "-c", voice_code, message], check=False)
    except Exception as error:
        print("Speech Error:", error)

def take_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            print("Recognizing...")
            command = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("You:", command)
            return command.lower()

        except sr.WaitTimeoutError:
            print("No voice detected.")
            return ""

        except sr.UnknownValueError:
            print("Speech was not clear.")
            return ""

        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""

        except Exception as error:
            print("Microphone error:", error)
            return ""


# -------------------------------
# GREETING FUNCTION
# -------------------------------

def wish_me():
    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good morning!")

    elif hour < 17:
        speak("Good afternoon!")

    else:
        speak("Good evening!")

    speak("Hello! I am Amigo, your voice assistant.")
    speak("How can I help you?")


# -------------------------------
# WEB SEARCH FUNCTION
# -------------------------------

last_search_url = ""


def search_web(topic):
    global last_search_url

    speak("Searching the internet for " + topic)

    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    topic,
                    max_results=8
                )
            )

        if not results:
            speak("Sorry, I could not find any results.")
            return

        # Remove duplicate titles
        unique_results = []
        seen_titles = set()

        for result in results:
            title = result.get("title", "").strip()
            summary = result.get("body", "").strip()
            link = result.get("href", "").strip()

            if title and title.lower() not in seen_titles:
                seen_titles.add(title.lower())

                unique_results.append({
                    "title": title,
                    "summary": summary,
                    "link": link
                })

        if not unique_results:
            speak("No useful results were found.")
            return

        # Select up to three results
        selected_results = unique_results[:3]

        speak("I found some information for you.")

        for index, result in enumerate(selected_results, start=1):
            title = result["title"]
            summary = result["summary"]
            link = result["link"]

            print("\nResult", index)
            print("Title:", title)
            print("Information:", summary)
            print("Link:", link)

            # UPDATED: Speak title and summary together
            if summary:
                speak(title + ". " + summary)
            else:
                speak(title)

            if link:
                last_search_url = link

        speak("That is the information I found.")

    except Exception as error:
        print("Search error:", error)
        speak("Sorry, I could not complete the web search.")


# -------------------------------
# WIKIPEDIA SEARCH
# -------------------------------

def search_wikipedia(topic):
    speak("Searching Wikipedia.")

    try:
        result = wikipedia.summary(
            topic,
            sentences=3,
            auto_suggest=True
        )

        print("\nWikipedia Information:")
        print(result)

        speak(result)

    except Exception:
        speak("I could not find information on Wikipedia.")
        search_web(topic)


# -------------------------------
# MAIN ASSISTANT FUNCTION
# -------------------------------

def run_amigo():
    wish_me()

    while True:
        command = take_command()

        if not command:
            continue

        # EXIT COMMANDS
        if any(word in command for word in [
            "exit", "stop", "quit", "goodbye",
            "shut down", "close amigo"
        ]):
            speak("Goodbye! Have a nice day.")
            break

        # GREETINGS
        elif any(word in command for word in [
            "hello", "hi", "hey"
        ]):
            speak("Hello! How can I help you?")

        # INTRODUCTION
        elif "who are you" in command or "your name" in command:
            speak("I am Amigo, your personal voice assistant.")
            speak("I can search the internet, tell the time, and open applications.")

        # HELP
        elif "help" in command or "what can you do" in command:
            speak(
                "I can search the internet, search Wikipedia, "
                "tell the time and date, open websites and applications, "
                "and tell jokes."
            )

        # TIME
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak("The current time is " + current_time)

        # DATE
        elif "date" in command or "today" in command:
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            speak("Today's date is " + current_date)

        # OPEN YOUTUBE
        elif "open youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        # OPEN GOOGLE
        elif "open google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        # OPEN NOTEPAD
        elif "open notepad" in command:
            speak("Opening Notepad.")
            import subprocess
            subprocess.Popen(["notepad.exe"])

        # OPEN CALCULATOR
        elif "open calculator" in command:
            speak("Opening Calculator.")
            import subprocess
            subprocess.Popen(["calc.exe"])

        # OPEN LAST SEARCH RESULT
        elif "open result" in command or "open last result" in command:
            if last_search_url:
                speak("Opening the last search result.")
                webbrowser.open(last_search_url)
            else:
                speak("There is no previous search result.")

        # SEARCH WIKIPEDIA
        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()

            if not topic:
                speak("Please tell me what you want to search on Wikipedia.")
            else:
                search_wikipedia(topic)

        # SEARCH GOOGLE / INTERNET
        elif "search for" in command:
            topic = command.replace("search for", "").strip()

            if topic:
                search_web(topic)
            else:
                speak("Please tell me what you want to search.")

        elif "search google for" in command:
            topic = command.replace("search google for", "").strip()

            if topic:
                search_web(topic)
            else:
                speak("Please tell me what you want to search.")

        # GENERAL QUESTIONS
        elif command.startswith("who is"):
            topic = command.replace("who is", "").strip()
            search_web(topic)

        elif command.startswith("what is"):
            topic = command.replace("what is", "").strip()
            search_web(topic)

        elif command.startswith("where is"):
            topic = command.replace("where is", "").strip()
            search_web(topic)

        elif command.startswith("how to"):
            topic = command.strip()
            search_web(topic)

        # JOKES
        elif "joke" in command:
            jokes = [
                "Why did the computer go to the doctor? Because it had a virus!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why was the computer cold? Because it left its Windows open!"
            ]

            speak(random.choice(jokes))

        # THANK YOU
        elif "thank you" in command or "thanks" in command:
            speak("You are welcome! I am always happy to help.")

        # HOW ARE YOU
        elif "how are you" in command:
            speak("I am doing great. Thank you for asking!")

        # UNKNOWN COMMAND
        else:
            speak("Sorry, I did not understand that command.")
            speak("Please try again.")


# -------------------------------
# START AMIGO
# -------------------------------

if __name__ == "__main__":
    try:
        run_amigo()

    except KeyboardInterrupt:
        speak("Amigo is closing. Goodbye!")

    except Exception as error:
        print("Assistant error:", error)
        speak("Something went wrong. Please try again.")
