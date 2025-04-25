import speech_recognition as sr 
import pyaudio
import wave
import tkinter as tk #replace with  (QT or pygame or something else looks better) (not doin allat)
from pathlib import Path
from allosaurus.app import read_recognizer
import threading
# Initialize the Allosaurus model and Tkinter window
model = read_recognizer('latest')
window = tk.Tk()









# define the transcription success variables
Transcriptionsucces = tk.StringVar()
Transcriptionsucces.set("False")
Photranscriptionsucces = tk.StringVar()
Photranscriptionsucces.set("Idle")
Wtranscription= tk.StringVar()
Wtranscription.set("")
Wptranscription= tk.StringVar()
Wptranscription.set("")

#goblin state variables and the tk shit to display it
goblinstate = "idle"
goblinstate_lock = threading.Lock()
goblinidlevariant = 1

idle1 = tk.PhotoImage(file="C:/Users/tomcr/Documents/projects/iteration2/idle1.png")
idle2 = tk.PhotoImage(file="C:/Users/tomcr/Documents/projects/iteration2/idle2.png")
idle3 = tk.PhotoImage(file="C:/Users/tomcr/Documents/projects/iteration2/idle3.png")
idle4 = tk.PhotoImage(file="C:/Users/tomcr/Documents/projects/iteration2/idle4.png")
idle5 = tk.PhotoImage(file="C:/Users/tomcr/Documents/projects/iteration2/idle5.png")
speaking1 = tk.PhotoImage(file="C:/Users/tomcr/Documents/projects/iteration2/speaking1.png")
speaking2 = tk.PhotoImage(file="C:/Users/tomcr/Documents/projects/iteration2/speaking2.png")
listening1 = tk.PhotoImage(file="C:/Users/tomcr/Documents/projects/iteration2/listening1.png")
dead = tk.PhotoImage(file= "C:/Users/tomcr/Documents/projects/iteration2/dead.png")


spritechange = tk.Label(window, image=idle1)
spritechange.pack()


class Audio: # i could fix the entire program freezing but that would involve me copying it from ai directly without understanding wtf is going on so i elected to not do that.
    def __init__(self):
        self.chunk = 1024
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 5

    def play_audio_introduction(self):
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
        return
    
    def play_audio_riddle(self):
        global goblinstate
        with goblinstate_lock:
            goblinstate = "speaking"
        
        wf = wave.open("riddle.wav", 'rb')

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
        
        #riddle play time
        goblinstate = "idle"
        return

    def record_audio(self):
        global goblinstate
        with goblinstate_lock:
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

        
        window.after(16000, lambda: setattr(goblinstate, "idle"))
        return

class Transcription:
    def __init__(self):
        self.PASSPHRASE = "folaki"
        self.PHOPASSPHRASES = ["f o l a k i", "f ɔ l ɑ k iʃ", "f ɔ l̪ l a k i", "f ɔ l a k i", "f o uə l a k̟ʲ i", "f ɔ ə l a k̟ʲ i", "f ɔ l̪ l a k̟ʲ i", "f a ʊ l ɑ k i"
                               , "f a l̪ h l ɑ k i", "f ɔ l a k̟ʲ i", "o l̪ lʲ a k̟ʲ i", "f a h l ɑ k i", "f a l̪ lʲ a k̟ʲ i", "f a l̪ l ɑ k i", "f ɔ ə l a ɡ i"
                               , "f ɔ h l a k̟ʲ i", "f ɔ l̪ l ɑ ɡ i", "f ɔ h l a k ɪ", "f ɔ lː a k̟ʲ i", "p ɔ l a k̟ʲ i", "p o l a k̟ʲ i", "f ɔ l̪ a k i"
                               , "f ɔ l a k ɪ", "f ɔ l a k ʰ i", "f ɔ l a k ʲ i", "f ɔ l ɑː k i", "f ɔ l ɑ k ɪ", "f ɔ l a k ɪʃ", "f ɔ l a kʰ i", "f ɔ l a k ɪ"
                               , "f ɔ l̪ l ɑː k i", "f ɔ l̪ l ɑ k ɪ", "f ɔ l aː k i", "f ɔ l̪ a kʰ i", "f ɔ l̪ a k ɪ", "f ɔ l̪ l a kʰ i", "f ɔ l̪ l a k ɪ"]

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
        self.Photranscription()
        return

class Goblinstatesetter:
    def __init__(self):
        pass

    def set_goblinstate(self, new_state):
        """Safely set the goblinstate using a lock."""
        global goblinstate
        with goblinstate_lock:
            goblinstate = new_state

    def get_goblinstate(self):
        """Safely get the current goblinstate using a lock."""
        global goblinstate
        with goblinstate_lock:
            return goblinstate


class Spritemanager:
    def __init__(self):
        self.state_setter = Goblinstatesetter()

    def setgoblinstateidle(self):
        global goblinidlevariant
        if self.state_setter.get_goblinstate() == "idle":
            if goblinidlevariant % 2 == 0:
                spritechange.config(image=idle1)
                window.after(1000, lambda: spritechange.config(image=idle2))
                window.after(2000, self.setgoblinstateidle)
            else:
                spritechange.config(image=idle3)
                window.after(1000, lambda: spritechange.config(image=idle4))
                window.after(2000, lambda: spritechange.config(image=idle5))
                window.after(2500, lambda: spritechange.config(image=idle4))
                window.after(3500, self.setgoblinstateidle)
            goblinidlevariant += 1
        else:
            return

    def setgoblinstatespeaking(self):
        if self.state_setter.get_goblinstate() == "speaking":
            spritechange.config(image=speaking1)
            window.after(1000, lambda: spritechange.config(image=speaking2))
            window.after(2000, self.setgoblinstatespeaking)
        else:
            return

    def setgoblinstatelistening(self):
        if self.state_setter.get_goblinstate() == "listening":
            spritechange.config(image=listening1)
            window.after(1000, self.setgoblinstatelistening)
        else:
            return
    def setgoblinstatedead(self):
            spritechange.config(image="C:/Users/tomcr/Documents/projects/iteration2/dead.png")
            window.after(1000, self.setgoblinstatedead)
            return


class Gamemanager:
    def __init__(self, event=None):
        self.state_setter = Goblinstatesetter()

    def play_intro(self, event=None):
        threading.Thread(target=self._play_intro_thread, daemon=True).start()

    def _play_intro_thread(self):
        self.state_setter.set_goblinstate("speaking")
        Audio().play_audio_introduction()
        self.state_setter.set_goblinstate("idle")

    def play_riddle(self, event=None):
        threading.Thread(target=self._play_riddle_thread, daemon=True).start()

    def _play_riddle_thread(self):
        Sprite = Spritemanager()
        self.state_setter.set_goblinstate("speaking")
        Sprite.setgoblinstatespeaking()
        Audio().play_audio_riddle()
        self.state_setter.set_goblinstate("idle")
        Sprite.setgoblinstateidle()

    def record_audio_analysis(self, event=None):
        threading.Thread(target=self._record_audio_thread, daemon=True).start()

    def _record_audio_thread(self):
        Sprite = Spritemanager()
        self.state_setter.set_goblinstate("listening")
        Sprite.setgoblinstatelistening()
        Audio().record_audio()
        self.state_setter.set_goblinstate("idle")
        Sprite.setgoblinstateidle()
        Transcription().transcribe_both()

def monitor_photranscriptionsucces():
    """Monitor the Photranscriptionsucces variable and trigger Gamefinished if it's True."""
    if Photranscriptionsucces.get() == "True":
        Pusher.send_game_finished_message()
        Spritemanager().setgoblinstatedead()
    else:
        # Check again after 100ms
        window.after(100, monitor_photranscriptionsucces)

# Start monitoring Photranscriptionsucces
monitor_photranscriptionsucces()

def interfaceboot():
    """Initialize the Tkinter interface."""
    Gamelogic = Gamemanager()
    Sprite = Spritemanager()
    window.title("Goblin Game")
    label = tk.Label(text="Hello, please speak the passphrase")
    label.pack()

    # Buttons for game actions
    button = tk.Button(
        text="Play Introduction",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=Gamelogic.play_intro
    )
    button.pack()

    button = tk.Button(
        text="Play Riddle",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=Gamelogic.play_riddle
    )
    button.pack()

    button = tk.Button(
        text="Record!",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=Gamelogic.record_audio_analysis
    )
    button.pack()

    # Display transcription success
    label4 = tk.Label(text="Success:")
    label4.pack()
    label5 = tk.Label(window, textvariable=Photranscriptionsucces)
    label5.pack()

    # Initialize the sprite in idle state
    Sprite.setgoblinstateidle()
    window.mainloop()


# Start the interface
interfaceboot()