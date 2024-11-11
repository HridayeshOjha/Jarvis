import speech_recognition as sr       # giving "sr" as a alternative  for calling speech_recognition
import webbrowser                     # allows to connect with web and dispaly its content
import pyttsx3                        # converts text to speech
import musicLibrary                   # calling music library that me made
import requests
import google.generativeai as genai
from datetime import datetime
from gtts import gTTS
import pygame
import os

recognizer=sr.Recognizer()        # creating object-"recognizer" which is going to recognise the speech that we are gonna say 
engine=pyttsx3.init()             # creating object-"engine" for intializing ptttsx3



def speak(text):              # functon for taking text and converting it into speech
    engine.say(text)
    engine.runAndWait()

# def speak(text):             # functon for taking text and converting it into speech in google voice
#     from gtts import gTTS
#     tts = gTTS(text)
#     tts.save('temp.mp3')

#     # Initializing pygame mixer
#     pygame.mixer.init()

#     # load the mp3 file
#     pygame.mixer.music.load('temp.mp3')

#     # play the mp3 file
#     pygame.mixer.music.play()

#     # keep the program running until the music stops playing
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

#     pygame.mixer.music.unload()

#     os.remove('temp.mp3')


def google_search(query):             # function for Google search
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    speak(f"Searching Google for {query}")



def AIprocess(command): 
    genai.configure(api_key="API_KEY")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("You are a virtual assistant named jarvis skilled in general tasks like alexa and google cloud who talks like jarvis from ironman and i am your master hridayesh ojha. Give short responses to my commands. "+command)
    responsegiven=response.text.replace("*"," ")
    print(responsegiven)
    return responsegiven




def processCommand(c):        #function for processing command
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open spotify" in c.lower():
        webbrowser.open("https://spotify.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("search"):
        search = c.lower().replace("search ", "")
        speak(f"searching {search}")
        google_search(search) 

    # elif c.lower().startswith("play"):
    #     song = c.lower().split(" ")[1]
    #     link = musicLibrary.music[song]
    #     webbrowser.open(link)

    elif "time" in c:  #command for time
        current_time = datetime.now().strftime("%I:%M %p")  # Format: HH:MM AM/PM
        speak(f"The current time is {current_time}")

    elif "date" in c:  #command for time
        todays_Date = datetime.now().strftime("%A, %B %d, %Y")  # Format: week , month dd, YYYY
        speak(f"Today is {todays_Date}")

    else:
        # gemini handle the request
        output = AIprocess(c)
        speak(output)



if __name__=="__main__":
    speak("Intializing Jarvis.....")

    while True:
        # listen for the wake word "jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
            word=r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("yes Sir..")
                # listen for command
                while True:
                  with sr.Microphone() as source:
                    print("jarvis Activated")
                    audio = r.listen(source, phrase_time_limit=10)
                    try:
                        command=r.recognize_google(audio)
                        if (command=="ok standby"):
                            processCommand(command)
                            break
                        if(command=="shutdown"):
                            processCommand(command)
                            exit()
                        processCommand(command)
                    except sr.UnknownValueError:
                            print("Sorry, I didn't catch that.")
                    except sr.RequestError as e:
                            print(f"Could not request results; {e}")


        except Exception as e:
            print("Error; {0}".format(e))
