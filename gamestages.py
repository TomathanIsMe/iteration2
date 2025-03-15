from Interface import interface
from variables import GAMESTATE


# Run the interface
interface()

# States for character changes
if GAMESTATE == "introduction":
    from audioRNP import play_audio
    play_audio()

if GAMESTATE == "recording":
    from audioRNP import record_audio
    record_audio()

if GAMESTATE == "transcribing":
    from transcription import transcribe_both
    transcribe_both()