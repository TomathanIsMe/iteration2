
import tkinter as tk

#set the pass phrase for the game and its phonetic alternatives
PASSPHRASE = "test"
PHOPASSPHRASES = ["t̪ʰ e t͡ʃ","t æ s̪","t ɛ s t"] #needs a real passphrase and their phonetic simularities

# Set the transcription variable for the hud
ENGtranscriptionsucces = tk.StringVar()
ENGtranscriptionsucces.set("False")
Photranscriptionsucces = tk.StringVar()
Photranscriptionsucces.set("False")
wENGtranscription= tk.StringVar()
wENGtranscription.set("")
wPHOtranscription= tk.StringVar()
wPHOtranscription.set("")

# Set the transcription variables for the game for usage outside of the tkinter interface
ENGLISHTRANSCRIPTIONSUCCES = ENGtranscriptionsucces
PHONETICTRANSCRIPTIONSUCCES = Photranscriptionsucces
ENGLISHTRANSCRIPTION = wENGtranscription
PHONETICTRANSCRIPTION = wPHOtranscription

# goblin state variable
GOBLINSTATE = "NEUTRAL"

GAMESTATE = ""  # Set the game state to blank