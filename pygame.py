import speech_recognition as sr 
import pyaudio
import wave
import tkinter as tk
from pathlib import Path
from allosaurus.app import read_recognizer


# Initialize the Allosaurus model Works
model = read_recognizer('latest')

# Define the passphrase
PASSPHRASE = "test"
PHOPASSPHRASES = ["t̪ʰ e t͡ʃ","t æ s̪"] #needs a real passphrase and their phonetic simularities

# Create a function to record audio
def record_audio():
    # Define audio parameters as variables (its needed for pyaudio to function)
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "recording.wav" 

    # Start pyaudio
    audio = pyaudio.PyAudio()

    # Open a recording buffer/stream like in sfml
    stream = audio.open(format=pyaudio.paInt16, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("listening")
    # Create a list to store audio chunks temporarily (optimisation)
    frames = []

    # Record audio in chunks to save memory (optimisation)
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("done listening")  # Stops the recording and notify the user (me)

    # Stop and close the stream
    stream.stop_stream()  # Stop recording
    stream.close()        # Close the stream "buffer"
    audio.terminate()     # Close the communication with the audio device

    # Save the audio data that has just been recorded to a file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # Opens a file to write the audio data to and sets it to write in binary mode (otherwise things break lmao)
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    return

# Create a function to convert the audio to text                        Remove when done debuggin, is not needed allosaurus is superior
def transcription():
    # Define the recognizer
    r = sr.Recognizer()

    # Open the audio file
    with sr.AudioFile("recording.wav") as source:
        audio = r.record(source)  # Record the audio file

    # Transcribe the audio
    try:
        transcription = r.recognize_google(audio)
        print("You said: " + transcription)  # Print the transcribed audio

        # Compare the transcription to the passphrase
        if PASSPHRASE.lower() in transcription.lower():
            print("The transcription contains the passphrase.")
        else:
            print("The transcription does not contain the passphrase.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return

def Photranscription():
    try:
        # Path to the audio file (didnt know how to fix it otherwise so just import more lmao)
        audio_file = Path("C:/Users/tomcr/Documents/projects/iteration2/recording.wav")
        # Use the already initialized model
        output = model.recognize(audio_file, "ipa")
        print(output)
        if any(phrase in output for phrase in PHOPASSPHRASES):
            print("The transcription contains the passphrase PHONETICALLY.")
        else:
            print("The transcription does not contain the passphrase.")
    except Exception as e:
        print(f"An error occurred during phonetic transcription: {e}")

#tk interface for user input hopefully (needs more learning)
window = tk.Tk()
label = tk.Label(text="Hello, Mario")
label.pack()
window.mainloop()


#User input prompting (basically here temporarily untill i have an interface or better idea)

input("Press enter to start recording")
record_audio()
input("Press enter to transcribe the audio")
transcription()
input("Press enter to transcribe the audio using Allosaurus")
Photranscription()
