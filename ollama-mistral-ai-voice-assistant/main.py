import time
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import ollama
import os

lang = 'en'

def speak(text):
    """Convert text to speech and play it."""
    print(f"Speaking: {text}")
    try:
        tts = gTTS(text=text, lang=lang, tld="com.au")
        tts.save("response.mp3")
        audio = AudioSegment.from_file("response.mp3", format="mp3")
        play(audio)
        os.remove("response.mp3")  # Clean up temporary file
    except Exception as e:
        print(f"Error in speak: {e}")

def get_audio():
    """Listen for audio input and process it."""
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            said = r.recognize_google(audio, language='en-US').lower()
            print(f"Heard: {said}")

            # Check for wake word
            if "java" in said:
                print("Trigger word detected")
                # Use Ollama Mistral model
                response = ollama.chat(
                    model="mistral:latest",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant providing concise and accurate answers."},
                        {"role": "user", "content": said}
                    ]
                )
                reply = response['message']['content'].strip()
                print(f"AI Response: {reply}")
                speak(reply)
            else:
                print("No trigger word detected")

        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def main():
    """Main loop for continuous listening."""
    print("Starting voice assistant with Ollama Mistral...")
    while True:
        try:
            get_audio()
            time.sleep(0.1)  # Prevent excessive CPU usage
        except KeyboardInterrupt:
            print("\nStopping voice assistant...")
            break

if __name__ == "__main__":
    main()