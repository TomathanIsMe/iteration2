from Interface import interface
from transcription import transcription, Photranscription, transcribe_both
from audioRNP import record_audio, play_audio
from variables import ENGLISHTRANSCRIPTION,ENGLISHTRANSCRIPTIONSUCCES,PHONETICTRANSCRIPTION,PHONETICTRANSCRIPTIONSUCCES

GAMESTATE = ""  # Set the game state to blank

# Run the interface
interface()

# States for character changes
if GAMESTATE == "introduction":
    play_audio()

if GAMESTATE == "recording":
    record_audio()

if GAMESTATE == "transcribing":
    transcribe_both()