import pyttsx3 # pip install pyttsx3
import datetime
import speech_recognition as sr # pip install speechRecognition
import wikipedia #pip install wikipedia
import pyjokes as joke #pip install pyjokes
import webbrowser as wb
import os
import random
from newsapi import NewsApiClient
import json
from urllib.request import urlopen
import requests

# Init
newsapi = NewsApiClient(api_key='2b71328bb53749509e8814fbd3a45512')# pip install newsapi-python

engine = pyttsx3.init()

#get current Year
def getCurrentYear():
    return datetime.datetime.now().year

#get current month
def getCurrentMonth():
    return datetime.datetime.now().strftime("%B")

#get current date
def getCurrentDay():
    return datetime.datetime.now().day

# getting a joke
def getAJoke():
    return joke.get_joke()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def speakTime():
    Time = datetime.datetime.now().strftime("%I:%M %p") # 12hrs time with am and PM
    speak("The current time is "+ Time)    

def speakDate():
    speak("Today's date is "+str(getCurrentDay())+getCurrentMonth()+str(getCurrentYear()))

def wishMe():
    speak("Welcome Shyam")
    speakTime()
    speakDate()

    hour = datetime.datetime.now().hour
    
    #greeting message
    greetingMsg = ""
    if hour>=6 and  hour <=12:
        greetingMsg = "Good morning Sir"
    elif hour>12 and hour<18:
        greetingMsg = "Good afternoon sir"
    elif hour>=18 and hour<24:
        greetingMsg = "Good evening Sir"
    else:
        greetingMsg = "Good night sir"    

    #adding some more texts to that 
    speak(greetingMsg)

    greetingMsg = "Your Jarvis at your service"
    speak(greetingMsg)
    greetingMsg ="please tell me how can I help you today?"
    speak(greetingMsg)

def TakeMyCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(query)
    except Exception as e:
        print(e)
        speak("Sorry sir, I could not undestand")
        speak("Please try again")
        return "None"
    return query

if __name__ == "__main__":
    wishMe()

    # take input from microphone
    command = TakeMyCommand().lower()

    # checking time
    if "time" in command and not "music" in command or "current time" in command or "the time" in command:
        speakTime()

    elif "the date" in command or "today date" in command or "date" in command:
        speakDate()    

    elif "wikipedia" in command or "on wikipedia" in command:
        speak("Okay searching on wikipedia")
        command = command.replace('wikipedia', '')
        try:
            result = wikipedia.summary(command, sentences=2)
            speak("According to wikipedia")
            print(result)
            speak(result)
        except Exception as e:
            print(e)
            speak("Sorry couldn't find data on wikipedia") 

    elif "joke" in command:
        joke = getAJoke()
        print(joke)
        speak(joke)

    elif "open in chrome" in command:
        speak("what should I open")
        chromePath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        command = TakeMyCommand().lower()
        wb.get(chromePath).open(command+".com")

    elif "search in google" in command:
        speak("what should I search")
        chromePath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        command = TakeMyCommand().lower()
        urlGoogle = "https://www.google.com/search?q="
        wb.get(chromePath).open(urlGoogle+command)    

    elif "search in youtube" in command:
        speak("what should I search")
        chromePath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        command = TakeMyCommand().lower()
        urlYoutube = "https://www.youtube.com/results?search_query="
        wb.get(chromePath).open(urlYoutube+command)  

    elif "bye" in command:
        speak("Good bye sirr!!!")
        speak("Have a good day")
        quit()    

    elif "word" in command:
        speak("Opening MS word")
        ms_word = "C:/Program Files (x86)/Microsoft Office/root/Office16/WINWORD.EXE"
        os.startfile(ms_word)

    elif "vs code" in command:
        speak("Opening VS Code")
        vsCode = "C:/Users/demo/AppData/Local/Programs/Microsoft VS Code/Code.exe"
        os.startfile(vsCode)

    elif "write a note" in command or "make a note" in command:
        speak("What should I write for you sir")
        note = TakeMyCommand().lower()

        speak("should I write date and time")
        dateTime = TakeMyCommand().lower()

        fileNote = open("notes.txt", "w")

        if "yes" in dateTime or "ok" in dateTime or "sure" in dateTime:
            date = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")
            speak("okay writing date")
            fileNote.write(date)
            fileNote.write(" :\n")

        fileNote.write(note+"\n--------------\n")
        speak("Your note has been saved sir")

    elif "show me notes" in command or "show notes" in command:
        fileNote = open("notes.txt", "r")
        noteContent = fileNote.read()
        speak("okay showing notes")
        print(noteContent)
        speak(noteContent)

    elif  "play songs" in command or "play music" in command or "music time" in command or "music" in command:
        speak("playing youtube")
        fav_songs = ["pxQyPsw3ro8&t=95", "87ErHaYgdtg&t=70", "VAZxSoKb65o&t=69", "ZTBwxy4wsBQ&t=202", "Ps4aVpIESkc&list=PL9bw4S5ePsEEqCMJSiYZ-KTtEjzVy0YvK", "Dt5GMToSu5I&t=21"]
        chromePath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        urlYoutube = "https://www.youtube.com/watch?v="
        randomDigit = random.randint(0, len(fav_songs))
        wb.get(chromePath).open(urlYoutube+fav_songs[randomDigit])

    elif "remember that" in command:
        speak("what you want me to remember")
        rememberContent =  TakeMyCommand()
        fileRemember = open("memory.txt", "w")
        fileRemember.write(rememberContent)
        speak("I have remembered that sir")

    elif "do you remember anything" in command:
        fileRemember = open("memory.txt",'r')
        fileContent = fileRemember.read()
        if(len(fileContent)>0):
            speak("Yes I have something in my memory")
            speak(fileContent)
        else:
            speak("No sir, I don't have anything in my memory")

    elif "news" in command or "headlines" in command:
        # /v2/top-headlines
        top_headlines = newsapi.get_top_headlines(sources='bbc-news',language='en')
        articles = top_headlines["articles"]
        titles = [article['title'] for article in articles]
        i = 1
        speak("fetching top 10 headlines sir")
        for title in titles:
            print(str(i) + ". "+title)
            speak(title)
            i+=1

    elif "what is the meaning of" in command:
        commandWord = command.replace("what is the meaning of ",'')  
        googleDictionaryAPI = "https://api.dictionaryapi.dev/api/v2/entries/en/"+commandWord
        try:
            jsonOutput = json.load(urlopen(googleDictionaryAPI))
            i=1
            listOfMeanings = jsonOutput[0]['meanings']
            listOfDefinitions = listOfMeanings[0]['definitions']
            listOfActualMeanings = [meaning['definition'] for meaning in listOfDefinitions]
            for meaning in listOfActualMeanings:
                print(str(i)+". "+meaning)
                speak(meaning)
                i+=1
        except Exception as e:
            print(e)
            speak("Sorry could not understand, please try again")

    elif "shutdown" in command:
        os.system("shutdown /s /t 1")

    elif "restart" in command:
        os.system("shutdown /r /t 1")    

    elif "log out" in command:
        os.system("shutdown -l")            


    

        

