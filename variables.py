
import tkinter as tk

#set the pass phrase for the game and its phonetic alternatives
PASSPHRASE = "test"
PHOPASSPHRASES = ["t̪ʰ e t͡ʃ","t æ s̪","t ɛ s t"] #needs a real passphrase and their phonetic simularities

# Set the transcription variable for the hud
Transcriptionsucces = tk.StringVar()
Transcriptionsucces.set("False")
Photranscriptionsucces = tk.StringVar()
Photranscriptionsucces.set("False")
Wtranscription= tk.StringVar()
Wtranscription.set("")
Wptranscription= tk.StringVar()
Wptranscription.set("")