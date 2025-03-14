import speech_recognition as sr 
import tkinter as tk
from pathlib import Path
from allosaurus.app import read_recognizer
from variables import Wptranscription, Wtranscription, Transcriptionsucces, Photranscriptionsucces, PASSPHRASE, PHOPASSPHRASES
from gamestages import GAMESTATE
from variables import GOBLINEMOTIONALSTATE

# Initialize the Allosaurus model and Tkinter window (so i can set the variables before they are used)
model = read_recognizer('latest')
window = tk.Tk()

def transcription():
    # Define the recognizer
    
    r = sr.Recognizer()
    # Open the audio file
    with sr.AudioFile("recording.wav") as source:
        audio = r.record(source)  # Record the audio file
        Wtranscription.set(r.recognize_google(audio)) #sets the transcription to a variable for the interface
    # Transcribe the audio
    try:
        transcription = r.recognize_google(audio)
        print("You said: " + transcription)  # Print the transcribed audio

        # Compare the transcription to the passphrase
        if PASSPHRASE.lower() in transcription.lower():
            print("The transcription contains the passphrase.")
            Transcriptionsucces.set("True") #used to display the game state outside of terminal
        else:
            print("The transcription does not contain the passphrase.")
            Transcriptionsucces.set("False") #used to display the game state outside of terminal

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return
# phonetic transcription using allosaurus
def Photranscription():
    global GOBLINEMOTIONALSTATE
    try:
        # Path to the audio file (didnt know how to fix it otherwise so just import more lmao)
        audio_file = Path("C:/Users/tomcr/Documents/projects/iteration2/recording.wav")
        # Use the already initialized model
        output = model.recognize(audio_file, "ipa")
        print(output)
        Wptranscription.set(output) #sets the transcription to a variable for the interface

        # Compare the transcription to the passphrase
        if any(phrase in output for phrase in PHOPASSPHRASES):
            print("The transcription contains the passphrase PHONETICALLY.")
            Photranscriptionsucces.set("True") #used to display the game state outside of terminal
            GOBLINEMOTIONALSTATE = "happy"
        else:
            print("The transcription does not contain the passphrase.")
            Photranscriptionsucces.set("False") #used to display the game state outside of terminal
            GOBLINEMOTIONALSTATE = "angry"
    except Exception as e:
        print(f"An error occurred during phonetic transcription: {e}")
    GOBLINEMOTIONALSTATE = "confused"
# combine them to run them at the same time (debuggin tool for now will be removed later) used mainly for testing phonetic vs english passphrases
def transcribe_both():
    transcription()
    Photranscription()