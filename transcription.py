import speech_recognition as sr 
import tkinter as tk
from pathlib import Path
from allosaurus.app import read_recognizer

from variables import GOBLINSTATE

# Initialize the Allosaurus model and Tkinter window (so i can set the variables before they are used)
model = read_recognizer('latest')

def transcription():
    #imports when the functions is called (avoid cicrular imports)
    from variables import ENGtranscriptionsucces, wENGtranscription
    from variables import PASSPHRASE

    r = sr.Recognizer()
    # Open the audio file
    with sr.AudioFile("recording.wav") as source:
        audio = r.record(source)  # Record the audio file
        wENGtranscription.set(r.recognize_google(audio)) #sets the transcription to a variable for the interface
    # Transcribe the audio
    try:
        transcription = r.recognize_google(audio)
        print("You said: " + transcription)  # Print the transcribed audio

        # Compare the transcription to the passphrase
        if PASSPHRASE.lower() in transcription.lower():
            print("The transcription contains the passphrase.")
            ENGtranscriptionsucces.set("True") #used to display the game state outside of terminal
        else:
            print("The transcription does not contain the passphrase.")
            ENGtranscriptionsucces.set("False") #used to display the game state outside of terminal

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return
# phonetic transcription using allosaurus
def Photranscription():
    # imports when the functions is called (avoid cicrular imports)
    from variables import wPHOtranscription, Photranscriptionsucces 
    from variables import PHOPASSPHRASES

    global GOBLINSTATE
    try:
        # Path to the audio file (didnt know how to fix it otherwise so just import more lmao)
        audio_file = Path("C:/Users/tomcr/Documents/projects/iteration2/recording.wav")
        # Use the already initialized model
        output = model.recognize(audio_file, "ipa")
        print(output)
        wPHOtranscription.set(output) #sets the transcription to a variable for the interface

        # Compare the transcription to the passphrase
        if any(phrase in output for phrase in PHOPASSPHRASES):
            print("The transcription contains the passphrase PHONETICALLY.")
            Photranscriptionsucces.set("True") #used to display the game state outside of terminal
            GOBLINSTATE = "happy"
        else:
            print("The transcription does not contain the passphrase.")
            Photranscriptionsucces.set("False") #used to display the game state outside of terminal
            GOBLINSTATE = "angry"
    except Exception as e:
        print(f"An error occurred during phonetic transcription: {e}")
    GOBLINSTATE = "confused"
# combine them to run them at the same time (debuggin tool for now will be removed later) used mainly for testing phonetic vs english passphrases
def transcribe_both():
    transcription()
    Photranscription()