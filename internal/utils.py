import json
from . import questions, hai_db, user_statistics_storage
from internal.gamemode import Gamemode

def get_next_question_id(username: str, gamemode: Gamemode) -> int:
    win, total = user_statistics_storage.Get(username, gamemode)
    return total  # 0-based question index

def get_data_by_id(data_id: int, gamemode: Gamemode) -> json:
    if gamemode == Gamemode.GUESS_THE_LVL:
        if data_id >= len(questions):
            print(f"WARNING: There is no data wit id {data_id} for gamemode {gamemode}")
            return None

        return questions[data_id]

    if gamemode == Gamemode.GUESS_HUMAN_OR_AI:
        if data_id >= len(hai_db):
            print(f"WARNING: There is no data wit id {data_id} for gamemode {gamemode}")
            return None

        return hai_db[data_id]

    print("WARNING: Unknown gamemode:", gamemode)
    return None
