import speech_recognition as sr 
import pyaudio
import wave
import tkinter as tk #replace with  (QT or pygame or something else looks better)
from pathlib import Path
from allosaurus.app import read_recognizer


# Initialize the Allosaurus model and Tkinter window
model = read_recognizer('latest')
window = tk.Tk()


# define the transcription success variables
Transcriptionsucces = tk.StringVar()
Transcriptionsucces.set("False")
Photranscriptionsucces = tk.StringVar()
Photranscriptionsucces.set("False")
Wtranscription= tk.StringVar()
Wtranscription.set("")
Wptranscription= tk.StringVar()
Wptranscription.set("")

#Game and goblin state variables
goblinstate = "idle"



class Audio:
    def __init__(self):
        self.chunk = 1024
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 5

    def play_audio(self):
        global goblinstate
        goblinstate = "speaking"
        wf = wave.open("introduction.wav", 'rb')

        audio = pyaudio.PyAudio()
        stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
        data = wf.readframes(self.chunk)
        while data != b'':
            stream.write(data)
            data = wf.readframes(self.chunk)
        stream.close()
        audio.terminate()
        goblinstate = "idle"
        return

    def record_audio(self):
        global goblinstate
        goblinstate = "listening"
        # Define audio parameters as variables (its needed for pyaudio to function)
        WAVE_OUTPUT_FILENAME = "recording.wav" 

        # Start pyaudio
        audio = pyaudio.PyAudio()

        # Open a recording buffer/stream like in sfml
        stream = audio.open(format=pyaudio.paInt16, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
        print("listening")
        # Create a list to store audio chunks temporarily (optimisation)
        frames = []

        # Record audio in chunks to save memory (optimisation)
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        print("done listening")  # Stops the recording and notify me (debugging)

        # Stop and close the stream
        stream.stop_stream()  # Stop recording
        stream.close()        # Close the stream "buffer"
        audio.terminate()     # Close the communication with the audio device (or something like that) i know what i mean

        # Save the audio data that has just been recorded to a file 
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # Opens a file to write the audio data to and sets it to write in binary mode (otherwise things break lmao)
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        goblinstate = "idle"
        return

class transcription:
    def __init__(self):
        self.PASSPHRASE = "folaki"
        self.PHOPASSPHRASES = ["f o l a k i","f ɔ l ɑ k iʃ","f ɔ l̪ l a k i","f ɔ l a k i","f o uə l a k̟ʲ i","f ɔ ə l a k̟ʲ i,ts o ʁ lʲ a ɡ i","f a ʊ h l ɑ k ɪ","f ɔ l̪ l a k̟ʲ i",
                               "f a ʊ l ɑ k i","f a l̪ h l ɑ k i","f ɔ l a k̟ʲ i","o l̪ lʲ a k̟ʲ i","f a h l ɑ k i","f a h l ɑ k i","f a l̪ lʲ a k̟ʲ i","f a l̪ l ɑ k i"]
    # Create a function to convert the audio to text                        Remove when done debuggin, is not needed allosaurus is superior
    '''
    def transcription(self):
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
            if self.PASSPHRASE.lower() in transcription.lower():
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
    '''
    # phonetic transcription using allosaurus
    def Photranscription(self):
        try:
            # Path to the audio file (didnt know how to fix it otherwise so just import more lmao)
            audio_file = Path("C:/Users/tomcr/Documents/projects/iteration2/recording.wav")
            # Use the already initialized model
            output = model.recognize(audio_file, "ipa")
            print(output)
            Wptranscription.set(output) #sets the transcription to a variable for the interface

            # Compare the transcription to the passphrase
            if any(phrase in output for phrase in self.PHOPASSPHRASES):
                print("The transcription contains the passphrase PHONETICALLY.")
                Photranscriptionsucces.set("True") #used to display the game state outside of terminal
            else:
                print("The transcription does not contain the passphrase.")
                Photranscriptionsucces.set("False") #used to display the game state outside of terminal
        except Exception as e:
            print(f"An error occurred during phonetic transcription: {e}")
    # combine them to run them at the same time (debuggin tool for now will be removed later) used mainly for testing phonetic vs english passphrases
    def transcribe_both(self):
        #self.transcription()
        self.Photranscription()
        return
def interfaceboot():
    #tk interface for user input hopefully (needs more learning) (probs use it as a debug tool later for now its the main window)
    audiocall= Audio()
    transcribecall = transcription()

    window.title("Goblin game")
    label = tk.Label(text="Hello please speak the passphrase")
    label.pack()
    button = tk.Button(
        text="play introduction",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=audiocall.play_audio
    )
    button.pack()

    button = tk.Button(
        text="Record!",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=audiocall.record_audio
    )
    button.pack()

    button = tk.Button(
        text="transcribe!",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=transcribecall.transcribe_both
        ) # cant have two functions in one button so i made a new one that combines the two
    button.pack()
    '''
    label0 = tk.Label(window, text="Transcription success:")
    label0.pack()
    label1 = tk.Label(window, textvariable=Transcriptionsucces)
    label1.pack()
    label2 = tk.Label(text="transcription:")
    label2.pack()
    label3 = tk.Label(window, textvariable=Wtranscription)
    label3.pack()
    '''
    label4 = tk.Label(text="Phonetic transcription success:")
    label4.pack()
    label5 = tk.Label(window, textvariable=Photranscriptionsucces)
    label5.pack()
    label6 = tk.Label(text="Phonetic transcription:")
    label6.pack()
    label7 = tk.Label(window, textvariable=Wptranscription)
    label7.pack()

    window.mainloop()

'''
def goblinstatemanager()
    if goblinstate == "idle":
        #set animation to idle
    elif goblinstate == "speaking":
        #set animation to speaking
    elif goblinstate == "listening":
        #set animation to listening
    elif
'''

interfaceboot()





























#User input prompting (basically here temporarily untill i have an interface or better idea) now for debugging
'''
input("Press enter to start recording")
record_audio()
input("Press enter to transcribe the audio")
transcription()
input("Press enter to transcribe the audio using Allosaurus")
Photranscription()
'''


#things still to do:
# - explore passphrase options (phonetic and normal)
# - out of game mechanics / deliverables
# - create game assets like art and sound