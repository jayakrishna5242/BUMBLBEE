from __future__ import with_statement
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import pywhatkit as kit
import sys
import pyautogui
import time
import operator
import requests

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)
# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source,timeout=30)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query
        except Exception as e:
            print("Say that again please...")
            speak("Say that again please...")
            return "None"
API_KEY =' AIzaSyCkflEigBa-J4R0RY8JgNlU6HYc3refo6Y'
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}'


# Generate response from the Gemini API
def generate_response(data):
    payload = {
        "contents": [{
            "parts": [{"text": data}]
        }]
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raises HTTPError for bad responses
        response_json = response.json()
        # Extract content from the API response
        text = response_json['candidates'][0]['content']['parts'][0]['text'].strip()

        # Limit response to 2 lines (by splitting at line breaks)
        lines = text.split('\n')  # Split the response into lines
        limited_text = '\n'.join(lines[:1])  # Join the first 2 lines

        return limited_text

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def main():
    speak("I am bublebee and i am here to help you to do ypur daily asks..........")
    while True:
        query = takeCommand().lower()
        if 'what is your name' in query:
            speak("my name is bumblebee. What can I do for you today?")
        elif 'who created you' in query:
            speak("I was created by a talented developer. They built me to assist you in your daily tasks.")


        #Changing voice

        elif "toggle voice" in query or "change voice" in query:
            speak("Changing voice...")
            voices = engine.getProperty('voices')
            current_voice = engine.getProperty('voice')

            if current_voice == voices[0].id:  # If the current voice is male
                engine.setProperty('voice', voices[1].id)  # Change to female
                speak("Voice changed to female.")
            else:  # If the current voice is female
                engine.setProperty('voice', voices[0].id)  # Change to male
                speak("Voice changed to male.")


        # Youtube Commands


        elif 'trending on youtube' in query:
            speak("Let me show you what's trending on YouTube.")
            webbrowser.open("https://www.youtube.com/feed/trending")
        elif 'youtube shorts' in query:
            speak("opening youtube shorts")
            webbrowser.open("https://www.youtube.com/shorts")
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com/")
            speak("opening youtube")
            time.sleep(2)
            speak("how can i help you here?")
            n = 1
            while n == 1:
                task = takeCommand().lower().strip()
                if 'search' in task:
                    task = task.replace('search', '')
                    speak("searching..." + task)
                    pyautogui.press('/')
                    time.sleep(1)
                    pyautogui.write(task)
                    time.sleep(1)
                    pyautogui.press('enter')
                elif 'scroll down' in task:
                    pyautogui.press('pgdn')
                    speak("scrolling down")
                elif 'scroll up' in task:
                    pyautogui.press('pgup')
                    speak("scrolling down")
                elif 'pause' in task:
                    pyautogui.press('space')
                elif 'full screen' in task:
                    pyautogui.press('f')
                elif 'forward' in task:
                    pyautogui.press('right')
                elif 'rewind' in task:
                    pyautogui.press('left')
                elif 'next video' in task:
                    pyautogui.press('n')
                elif 'previous video' in task:
                    pyautogui.press('p')
                elif 'pause' or 'play' in task:
                    pyautogui.press('k')
                elif 'mute' in task:
                    pyautogui.press('m')
                elif 'close' in task:
                    speak('closing youtube')
                    n=0
                    pyautogui.hotkey('alt','f4')



        #Browser Commands
        elif 'open browser' in query:
            webbrowser.open("https://search.brave.com")
            speak("Opening Your Default browser...")
            pyautogui.hotkey('alt', 'space')  # Opens the window control menu
            pyautogui.press('x')

            n = 1
            speak("how can i  assist you in the browser")
            while n == 1:
                task = takeCommand().lower()
                if 'new tab' in task:
                    pyautogui.hotkey('ctrl', 'n')
                    speak('opening new tab ')

                elif 'incognito tab' in task:
                    pyautogui.hotkey('ctrl', 'shift', 'n')
                    speak('new incognito tab opened')
                elif 'history' in task:
                    pyautogui.hotkey('ctrl', 'h')
                    speak('your history is here')

                # Open downloads
                elif 'downloads' in task:
                    pyautogui.hotkey('ctrl', 'j')
                    speak('your downloads are here')

                # Switch to the previous tab
                elif 'previous tab' in task:
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                    speak('opening previous tab ')
                # Switch to the next tab
                elif 'next tab' in task:
                    pyautogui.hotkey('ctrl', 'tab')
                    speak('opening next tab ')

                # Close the current tab
                elif 'close tab' in task:
                    pyautogui.hotkey('ctrl', 'w')
                    speak('closing current tab ')

                # Close the Chrome window
                elif 'close window' in task:
                    pyautogui.hotkey('ctrl', 'shift', 'w')

                    # Clear browsing history
                elif 'clear browsing history' in task:
                    pyautogui.hotkey('ctrl', 'shift', 'delete')


                elif 'back' in task:
                    pyautogui.hotkey('alt', 'left')
                elif 'forward' in task:
                    pyautogui.hotkey('alt', 'right')
                elif 'search' in task:
                    task = task.replace('search', '')
                    webbrowser.open("https://search.brave.com/search?q=" + task)
                # Close Chrome entirely
                elif 'close browser' in task:
                    pyautogui.hotkey('alt', 'f4')
                    speak("browser closed")
                    n = 0


        #System Commands


        #opening Window
        elif 'open windows' in query:
            speak("Opening Windows.")
            pyautogui.hotkey('win')

        # Opening all applications

        elif 'open the application'  in query:
            query=query.replace('open the application', '')
            speak("Opening  "+ query)
            pyautogui.hotkey('win')
            time.sleep(0.2)
            pyautogui.write(query)
            time.sleep(0.2)
            pyautogui.press('enter')


        # Check battery status
        elif 'check battery status' in query:
            speak("Checking battery status.")
            os.system("powercfg /batteryreport")

        # Check system performance
        elif 'check system performance' in query:
            speak("Checking system performance.")
            os.system("perfmon")


        # Check disk space

        elif 'check disk space' in query:
            speak("Checking disk space.")
            os.system("wmic logicaldisk get size,freespace,caption")

        # Empty Recycle Bin

        elif 'empty recycle bin' in query:
            speak("Emptying Recycle Bin.")
            os.system("rd /s /q C:\\$Recycle.Bin")

        #Adjusting System Components


        # Adjust system volume

        elif 'increase volume' in query:
            speak("Increasing system volume.")
            pyautogui.press('volumeup', presses=5, interval=0.1)  # Press 5 times with interval

        elif 'decrease volume' in query:
            speak("Decreasing system volume.")
            pyautogui.press('volumedown', presses=5, interval=0.1)  # Press 5 times with interval

        elif 'mute volume' in query:
            speak("Muting system volume.")
            pyautogui.press('volumemute')


        #commands for windows

        # Minimize all windows
        elif 'minimise all windows' in query:
            speak("Minimizing all windows.")
            pyautogui.hotkey('win', 'd')

        # Maximize all windows
        elif 'maximize all windows' in query:
            speak("Maximizing all windows.")
            pyautogui.hotkey('win', 'd')

         # Minimize current window
        elif 'minimise current window' in query:
            speak("Minimizing current window.")
            pyautogui.hotkey('alt', 'tab')
            pyautogui.press('n')


        # Maximize all windows
        elif 'maximize current window' in query:
            pyautogui.hotkey('alt', 'space')
            pyautogui.press('x')

        #User Commands for System
        # Log off
        elif 'log off' in query:
            speak("Logging off.")
            os.system("shutdown /l")

        #Locking System
        elif 'lock the system' in query:
            pyautogui.hotkey('lock')

        #Shut Down System
        elif "shut down the system" in query:
            speak("Shutting down the system")
            os.system("shutdown /s /t 5")

        #Restrart System
        elif "restart the system" in query:
            speak("System is going to restart")
            os.system("shutdown /r /t 5")

        #Sleep System
        elif "sleep the system" in query:
            speak("System is going to sleep")
            os.system("powercfg -h off")  # Disable hibernation
            os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")

        #Hibernate System
        elif 'hibernate the system' in query:
            speak("Hibernating the system.")
            os.system("shutdown /h")


        #Closing the program
        # elif 'close the program ' or 'exit the program ' or 'stop the program' in query:
        #     speak("thank you ............have a nice day")
        #     break

        else:
            result = generate_response(query)
            # Generate API response and display
            print("BUMBLEBEE:", result)
            speak(result)

if __name__ == "__main__":
    main()