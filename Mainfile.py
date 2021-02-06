import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
# import vlc
import urllib
# import urllib2
import urllib.request as urllib2
import json
from bs4 import BeautifulSoup as soup

# import pyaudio
# from urllib2 import urlopen
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib import urlopen
import wikipedia
import random
from time import strftime
import pyttsx3

#Building a voice assistant
'''
        Supported commands :

        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
        4. Tell a joke/another joke : Says a random dad joke.
        5. Current weather in {cityname} : Tells you the current condition and temperture
        7. Hello
        8. play me a video : Plays song in your VLC media player
        9. change wallpaper : Change desktop wallpaper
        10. news for today : reads top news of today
        11. time : Current system time
        12. top stories from google news (RSS feeds)
        13. tell me about xyz : tells you about xyz
'''

def textToSpeech(textInput):
    # initialisation
    engine = pyttsx3.init()
    engine.say(textInput)
    engine.runAndWait()

def sofiaResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        textToSpeech(audio)
    # for line in audio.splitlines():
    #     os.system("say " + line)

def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def assistant(command):
    try:
        "if statements for executing commands"
        openGoogle = 'open google'
        # open subreddit Reddit
        if openGoogle in command:
            reg_ex = re.search(openGoogle + '(.*)', command)
            url = 'https://www.google.com/'
            if reg_ex:
                subreddit = reg_ex.group(1)
                # url = url + 'r/' + subreddit
            webbrowser.open(url)
            sofiaResponse('The ' + openGoogle + ' has been opened for you Sir.')

        elif 'sleep' in command:
            sofiaResponse('Bye bye Sir. Have a nice day')
            sys.exit()

        # open website
        elif 'open' in command:
            reg_ex = re.search('open (.+)', command)
            if reg_ex:
                domain = reg_ex.group(1)
                print(domain)
                url = 'https://www.' + domain
                webbrowser.open(url)
                sofiaResponse('The website you have requested has been opened for you Sir.')
            else:
                pass

        # greetings
        elif 'hey jarvis' in command:
            day_time = int(strftime('%H'))
            if day_time < 12:
                sofiaResponse('Hello Sir. Good morning')
            elif 12 <= day_time < 18:
                sofiaResponse('Hello Sir. Good afternoon')
            else:
                sofiaResponse('Hello Sir. Good evening')

        elif 'who am i' in command:
            sofiaResponse("Sir, Your name is wasique haidry")
        elif 'help me' in command:
            sofiaResponse("""
                You can use these commands and I'll help you out:

                1. Open reddit subreddit : Opens the subreddit in default browser.
                2. Open xyz.com : replace xyz with any website name
                3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
                4. Tell a joke/another joke : Says a random dad joke.
                5. Current weather in {cityname} : Tells you the current condition and temperture
                7. Greetings
                8. play me a video : Plays song in your VLC media player
                9. change wallpaper : Change desktop wallpaper
                10. news for today : reads top news of today
                11. time : Current system time
                12. top stories from google news (RSS feeds)
                13. tell me about xyz : tells you about xyz
                """)



        # time
        elif 'time' in command:
            import datetime
            now = datetime.datetime.now()
            sofiaResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))


        # play youtube song
        elif 'play me a song' in command:
            path = 'C:\\Users\\faraz.naqvi\\Downloads'
            folder = path
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        print(file_path)
                except Exception as e:
                    print(e)

            sofiaResponse('What song shall I play Sir?')
            mysong = myCommand()
            if mysong:
                flag = 0
                url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
                response = urllib2.urlopen(url)
                html = response.read()
                soup1 = soup(html, "lxml")
                url_list = []
                for vid in soup1.findAll(attrs={'class': 'yt-uix-tile-link'}):
                    if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                        flag = 1
                        final_url = 'https://www.youtube.com' + vid['href']
                        url_list.append(final_url)

                url = url_list[0]
                ydl_opts = {}

                os.chdir(path)
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                vlc.play(path)

                if flag == 0:
                    sofiaResponse('I have not found anything in Youtube ')

        # change wallpaper
        elif 'change wallpaper' in command:
            folder = '/Users/nageshsinghchauhan/Documents/wallpaper/'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            api_key = '***************'
            url = 'https://api.unsplash.com/photos/random?client_id=' + api_key  # pic from unspalsh.com
            f = urllib2.urlopen(url)
            json_string = f.read()
            f.close()
            parsed_json = json.loads(json_string)
            photo = parsed_json['urls']['full']
            urllib.urlretrieve(photo,
                               "/Users/nageshsinghchauhan/Documents/wallpaper/a")  # Location where we download the image to.
            subprocess.call(["killall Dock"], shell=True)
            sofiaResponse('wallpaper changed successfully')

        # ask me anything
        elif 'tell me about' in command:
            reg_ex = re.search('tell me about (.*)', command)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    ny = wikipedia.page(topic)
                    sofiaResponse(ny.content[:500].encode('utf-8'))
            except Exception as e:
                print(e)
                sofiaResponse(e)
        else:
            sofiaResponse('Sir. I dont have answer to that, Sorry')
    except:
        print("Thanks")


# sofiaResponse('Hi User, I am Sophia and I am your personal voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')
sofiaResponse('Hello wasique i am your personal trait seeker' )
#loop to continue executing multiple commands
while True:
    assistant(myCommand())
