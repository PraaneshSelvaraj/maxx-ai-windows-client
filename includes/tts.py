import os
from time import sleep
import json
from playsound import playsound
from gtts import gTTS
import pyttsx3
import winsound

engine = pyttsx3.init()

with open("./assets/config.json","r") as f:
    user_config = json.load(f)
f.close()

def speak(txt):
    if user_config['defaults']['voice_engine'] == 'pyttsx3':
        engine.say(txt)
        engine.runAndWait()
        return

    elif user_config['defaults']['voice_engine'] == 'gTTS':
        tts=gTTS(txt,lang='en',tld=user_config['defaults']['voice'])
        tts.save('output.mp3')
        sleep(0.5)
        print(txt)
        playsound("output.mp3")
        os.remove("output.mp3")

    elif user_config['defaults']['voice_engine'] == 'wit.ai':
        audio= requests.post(
        'https://api.wit.ai/synthesize',
        params={
            'v': '20220622',
        },
        headers={
            'Authorization': 'Bearer {}'.format(keys.wit_access_token),
        },
        json={ 'q': txt, 'voice': user_config['defaults']['voice'] },
        )

        with open("output.wav","wb") as f:
            f.writelines(audio)
        f.close()
        
        print(txt)
        winsound.PlaySound("output.wav", winsound.SND_FILENAME)
        os.remove("output.wav")