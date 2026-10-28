# Amigo – Python Voice Assistant

Amigo is a simple voice-controlled desktop assistant developed using Python. It listens to voice commands, responds through speech, searches Wikipedia, opens popular websites, and accesses available local drives.

## Features

- Voice input using the computer's microphone.
- Voice responses using text-to-speech.
- Wikipedia search with short summaries.
- Opens Google, YouTube, GitHub, Stack Overflow, Spotify, and WhatsApp Web.
- Opens available local drives (C, D, and E).
- Supports exit commands such as "exit", "quit", and "stop".
- Recognizes English (India) speech.

## Technologies Used

- Python 3
- SpeechRecognition
- PyAudio
- pyttsx3
- Wikipedia
- Webbrowser
- OS module

## Requirements

- Windows operating system
- Python 3.8 or later
- Microphone and speakers
- Internet connection for speech recognition and Wikipedia searches

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Anjalidasa344/voice-Assit.git
   ```

2. Open the project folder:

   ```bash
   cd voice-Assit
   ```

3. Install the required packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

## How to Run

Run the following command:

```bash
python amigo.py
```

Amigo will start listening for your voice commands.

## Available Voice Commands

| Voice Command | Action |
|---|---|
| "Open Google" | Opens Google |
| "Open YouTube" | Opens YouTube |
| "Open GitHub" | Opens GitHub |
| "Open Stack Overflow" | Opens Stack Overflow |
| "Open Spotify" | Opens Spotify |
| "Open WhatsApp" | Opens WhatsApp Web |
| "Wikipedia Python" | Searches Wikipedia for Python |
| "Local disk C" | Opens local disk C |
| "Local disk D" | Opens local disk D |
| "Local disk E" | Opens local disk E |
| "Who are you?" | Introduces Amigo |
| "Exit" | Closes the assistant |

## Project Structure

```text
Voice-Assistant/
│
├── amigo.py
├── README.md
├── requirements.txt
└── .gitignore
```

## How It Works

1. Amigo captures voice input through the microphone.
2. SpeechRecognition converts the voice into text using Google's speech recognition service.
3. The program checks the recognized text against available commands.
4. It performs the requested action.
5. pyttsx3 converts the response into speech.

## Future Improvements

- Add more voice commands.
- Support multiple languages.
- Add weather information.
- Improve command recognition and error handling.
- Add a graphical user interface.

## Acknowledgements

- Python
- SpeechRecognition
- PyAudio
- pyttsx3
- Wikipedia API

---

**Note:** This project uses online Google Speech Recognition and requires an internet connection for speech recognition and Wikipedia searches. Text-to-speech uses pyttsx3 with the Windows SAPI5 engine.