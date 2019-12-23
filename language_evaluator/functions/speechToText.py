import speech_recognition as sr
from pydub import AudioSegment
import shutil
from django.conf import settings
from os import path as p
from os import mkdir


def text_from_speech(file, username):
    uploads = '\\uploads\\'
    path = settings.MEDIA_ROOT + uploads
    if not p.exists(path):
        mkdir(path)
    filename = path + username + '.audio'
    filename_converted = filename + '.converted'
    with open(filename, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    AudioSegment.from_file(filename).export(filename_converted, format="wav")
    recognizer = sr.Recognizer()
    speech = sr.AudioFile(filename_converted)
    audio = None
    with speech as source:
        audio = recognizer.record(source)
    try:
        transcription = recognizer.recognize_google(audio, language='en-US')
    except sr.UnknownValueError:
        transcription = "Error"
    except sr.RequestError:
        transcription = "Error"
    return transcription
