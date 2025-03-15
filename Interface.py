import tkinter as tk

# Initialize the Tkinter window
window = tk.Tk()

def setgamestateintroduction():
    global GAMESTATE
    GAMESTATE = "introduction"
    return

def setgamestaterecording():
    global GAMESTATE
    GAMESTATE = "recording"
    return

def setgamestatetranscribe():
    global GAMESTATE
    GAMESTATE = "transcribing"
    return

def interface():
    # Imports when the function is called (avoid circular imports)
    from variables import wPHOtranscription, wENGtranscription, ENGtranscriptionsucces, Photranscriptionsucces

    label = tk.Label(text="Hello please speak the passphrase")
    label.pack()

    button = tk.Button(
        text="play introduction",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=setgamestateintroduction
    )
    button.pack()

    button = tk.Button(
        text="Record!",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=setgamestaterecording
    )
    button.pack()

    button = tk.Button(
        text="transcribe!",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=setgamestatetranscribe
    ) # cant have two functions in one button for some fuckin reason, so i made a new one that combines the two
    button.pack()

    label0 = tk.Label(window, text="Transcription success:")
    label0.pack()
    label1 = tk.Label(window, textvariable=ENGtranscriptionsucces)
    label1.pack()
    label2 = tk.Label(text="transcription:")
    label2.pack()
    label3 = tk.Label(window, textvariable=wENGtranscription)
    label3.pack()

    label4 = tk.Label(text="Phonetic transcription success:")
    label4.pack()
    label5 = tk.Label(window, textvariable=Photranscriptionsucces)
    label5.pack()
    label6 = tk.Label(text="Phonetic transcription:")
    label6.pack()
    label7 = tk.Label(window, textvariable=wPHOtranscription)
    label7.pack()

    window.mainloop()

# User input prompting (basically here temporarily until I have an interface or better idea)
'''
input("Press enter to start recording")
record_audio()
input("Press enter to transcribe the audio")
transcription()
input("Press enter to transcribe the audio using Allosaurus")
Photranscription()
'''

# Things still to do:
# - Make the interface look better
# - Explore passphrase options (phonetic and normal)
# - Out of game mechanics / deliverables
# - Create audio file as initial speech
# - Create game mechanics like failure system etc
# - Create game assets like art
# - Research Docker... for OpenAI's Whisper, kijk naar Raymond's bericht