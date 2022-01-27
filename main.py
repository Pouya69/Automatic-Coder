# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3
import datetime

# Initialize the recognizer
r = sr.Recognizer()
# engine = pyttsx3.init()
# engine.runAndWait()
log = ""


# Function to convert text to speech
def speak_text(command):
    engine.say(command)
    engine.runAndWait()


def listen():
    query = ""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')

    except:
        print("Sorry i didn't catch that...")
        return ""
    return query.lower()


if __name__ == '__main__':
    while True:
        text = listen()
        print(text + "\n")

        if text == "tell me a joke":
            answer = "Balls"
            log = log + f"\n>>Bot Answered: {answer}"
            print("[*] Balls")
        elif text == "exit" or text == "stop the program" or text == "stop listening":
            print("[*] Stopping the program...")
            break
        if not text == "":
            log = log + f"\n=>User said: {text}"

    file_name = f"output_log_{datetime.datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}.txt"
    print(f"writing the log file: {file_name}")
    with open(file_name, "w") as file:
        file.write(log)
    print("[!] Exiting the program...")
