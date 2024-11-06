import json
from . import questions
from . import hai_db

def get_next_question_id(user_id) -> int:
    # TODO: запрашиваем информацию из БД или файла
    return 0

def get_data_by_id(code_id: int) -> json:
    return hai_db[code_id]

def get_question_by_id(question_id) -> json:
    """
    questions.json format:
    {
        "code": string
        "is_level": bool
        "level": string
        "link": string
        "author": string
    }
    """
    if question_id >= len(questions):
        print("There is no question with id:", question_id)
        return None
    return questions[question_id]