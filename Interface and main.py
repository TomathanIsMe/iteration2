import tkinter as tk
from pathlib import Path
from audioRNP import play_audio, record_audio
from transcription import transcription, Photranscription, transcribe_both, Wptranscription, Wtranscription, Transcriptionsucces, Photranscriptionsucces


window = tk.Tk()

def interface():
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
    ) # cant have two functions in one button for some fuckin reason, so i made a new one that combines the two
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



#things still to do:
make the interface look better
explore passphrase options (phonetic and normal)
out of game mechanics / deliverables
create audio file as initial speech
create game mechanics like failure system etc
create game assets like art

research docker... for open ai's whisper, kijk naar raymonds bericht

'''