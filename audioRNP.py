import pyaudio
import wave

from variables import GOBLINSTATE

def play_audio():
    global GOBLINSTATE
    GOBLINSTATE = "Speaking"
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
    GOBLINSTATE = "Neutral"
    return

# Create a function to record audio
def record_audio():
    global GOBLINSTATE
    GOBLINSTATE = "Listening"
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
    GOBLINSTATE = "Neutral"
    return