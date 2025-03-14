from Interface import interface
from transcription import transcription, Photranscription, transcribe_both
from audioRNP import record_audio, play_audio
from variables import ENGLISHTRANSCRIPTION,ENGLISHTRANSCRIPTIONSUCCES,PHONETICTRANSCRIPTION,PHONETICTRANSCRIPTIONSUCCES

GAMESTATE = "INTRODUCTION"  # Set the game state to introduction

# Run the interface
interface()

# States for character changes
GOBLINEMOTIONALSTATE = "NEUTRAL"