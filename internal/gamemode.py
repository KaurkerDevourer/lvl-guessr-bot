from enum import Enum
from collections import defaultdict

class Gamemode(Enum):
    GUESS_THE_LVL = 0
    AI_VS_HUMAN = 1

def to_string(gamemode: Gamemode) -> str:
    if gamemode == Gamemode.GUESS_THE_LVL:
        return "Guess the Level"
    if gamemode == Gamemode.AI_VS_HUMAN:
        return "Human or AI"
    
    print("WARNING: Unknown gamemode:", gamemode)
    return "Unknown"
