import speech_recognition as sr 
import pyaudio
import wave
import tkinter as tk #replace with  (QT or pygame or something else looks better)
from pathlib import Path
from allosaurus.app import read_recognizer


# Initialize the Allosaurus model and Tkinter window (so i can set the variables before they are used)
model = read_recognizer('latest')
window = tk.Tk()

# Define the passphrase
PASSPHRASE = "test"
PHOPASSPHRASES = ["t̪ʰ e t͡ʃ","t æ s̪"] #needs a real passphrase and their phonetic simularities

# define the transcription success variables
Transcriptionsucces = tk.StringVar()
Transcriptionsucces.set("False")
Photranscriptionsucces = tk.StringVar()
Photranscriptionsucces.set("False")
Wtranscription= tk.StringVar()
Wtranscription.set("")
Wptranscription= tk.StringVar()
Wptranscription.set("")


# Create a function to play audio
def play_audio():
    chunk = 1024
    wf = wave.open("introduction.wav", 'rb')

    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
    data = wf.readframes(chunk)
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()
    audio.terminate()
    return
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
    print("done listening")  # Stops the recording and notify me (debugging)

    # Stop and close the stream
    stream.stop_stream()  # Stop recording
    stream.close()        # Close the stream "buffer"
    audio.terminate()     # Close the communication with the audio device (or something like that) i know what i mean

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
        else:
            print("The transcription does not contain the passphrase.")
            Photranscriptionsucces.set("False") #used to display the game state outside of terminal
    except Exception as e:
        print(f"An error occurred during phonetic transcription: {e}")
# combine them to run them at the same time (debuggin tool for now will be removed later) used mainly for testing phonetic vs english passphrases
def transcribe_both():
    transcription()
    Photranscription()

#tk interface for user input hopefully (needs more learning) (probs use it as a debug tool later for now its the main window)
label = tk.Label(text="Hello please speak the passphrase")
label.pack()
button = tk.Button(
    text="play introduction",
    width=25,
    height=5,
    bg="white",
    fg="black",
    command=play_audio
)
button.pack()

button = tk.Button(
    text="Record!",
    width=25,
    height=5,
    bg="white",
    fg="black",
    command=record_audio
)
button.pack()

button = tk.Button(
    text="transcribe!",
    width=25,
    height=5,
    bg="white",
    fg="black",
    command=transcribe_both
    ) # cant have two functions in one button so i made a new one that combines the two
button.pack()

label0 = tk.Label(window, text="Transcription success:")
label0.pack()
label1 = tk.Label(window, textvariable=Transcriptionsucces)
label1.pack()
label2 = tk.Label(text="transcription:")
label2.pack()
label3 = tk.Label(window, textvariable=Wtranscription)
label3.pack()

label4 = tk.Label(text="Phonetic transcription success:")
label4.pack()
label5 = tk.Label(window, textvariable=Photranscriptionsucces)
label5.pack()
label6 = tk.Label(text="Phonetic transcription:")
label6.pack()
label7 = tk.Label(window, textvariable=Wptranscription)
label7.pack()
window.mainloop()


#User input prompting (basically here temporarily untill i have an interface or better idea)
'''
input("Press enter to start recording")
record_audio()
input("Press enter to transcribe the audio")
transcription()
input("Press enter to transcribe the audio using Allosaurus")
Photranscription()
'''


#things still to do:
# - make the interface look better
# - explore passphrase options (phonetic and normal)
# - out of game mechanics / deliverables
# - create audio file as initial speech
# - create game mechanics like failure system etc
# - create game assets like art