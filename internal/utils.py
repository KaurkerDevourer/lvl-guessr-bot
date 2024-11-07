import json
from . import questions, hai_db, user_statistics_storage
from internal.gamemode import Gamemode

def get_next_question_id(user_id: str, gamemode: Gamemode) -> int:
    win, total = user_statistics_storage.Get(user_id, gamemode)
    return total  # 0-based question index

def get_data_by_id(code_id: int) -> json:
    if code_id >= len(hai_db):
        print("There is no data with id:", code_id)
        return None
    return hai_db[code_id]

def get_question_by_id(question_id) -> json:
    if question_id >= len(questions):
        print("There is no question with id:", question_id)
        return None
    return questions[question_id]
