import pyttsx3 # pip install pyttsx3
engine = pyttsx3.init()
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
