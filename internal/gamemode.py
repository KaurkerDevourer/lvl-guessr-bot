from enum import Enum
from collections import defaultdict

class Gamemode(Enum):
    GUESS_HUMAN_OR_AI = 0
    GUESS_THE_LVL = 1
    CHALLENGE = 2

def pretty_name(gamemode: Gamemode) -> str:
    if gamemode == Gamemode.GUESS_THE_LVL:
        return "🎮 Guess the Level"
    if gamemode == Gamemode.GUESS_HUMAN_OR_AI:
        return "🤖 Guess: Human or AI"
    if gamemode == Gamemode.CHALLENGE:
        return "CHALLENGE"

    print("WARNING: Unknown gamemode:", gamemode)
    return "Unknown"
