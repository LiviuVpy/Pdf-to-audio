
from dotenv import load_dotenv
import requests
import os

#  import the environment variables form the .env file
load_dotenv("pdf_to_audio_API\.env")

class DataManager():
    '''creates the blueprint for an object in ui.py '''
    def __init__(self, voice, source):
        self.endpoint = os.environ["VOICERSS_ENDPOINT"]
        self.api_key = os.environ["VOICERSS_API_KEY"]
        self.voice = voice
        self.source = source

    def get_mp3(self):
        '''sets the parameters and the request to voicerss API
        writes the mp3 file on disk'''
        parameters = {
            "key" : self.api_key,
            "src" : self.source,
            "hl" : "en-us",
            "c" : "MP3",
            "f" : "16khz_16bit_stereo",
            'v': self.voice,
        }

        audio_response = requests.get(url=self.endpoint, params=parameters)
        if audio_response.status_code == 200:
            with open('pdf_to_audio_API\\sound_file.mp3', 'wb') as f:
                f.write(audio_response.content)
        else:
            print(audio_response.text)
