import json
from enum import Enum
from collections import defaultdict


class UseCase(Enum):
    GUESS_THE_LVL = 0
    AI_VS_HUMAN = 1


class UserStatisticsStorage:
    def __init__(self):
        with open("db/user_statistics.json", "r") as file:
            raw_data = json.loads(file.read())

        self.data = defaultdict(lambda: defaultdict(lambda: (0, 0)))
        for (user_id, stat) in raw_data.items():
            self.data[user_id] = defaultdict(lambda: (0, 0), stat)

    def AddWin(self, user_id: str, use_case: UseCase):
        """Example of a call: stat.add_win("user_id", UseCase.GUESS_THE_LVL)"""
        (win, total) = self.data[user_id][use_case.name]
        self.data[user_id][use_case.name] = (win + 1, total + 1)

    def AddFail(self, user_id: str, use_case: UseCase):
        (win, total) = self.data[user_id][use_case.name]
        self.data[user_id][use_case.name] = (win, total + 1)

    def Get(self, user_id: str, use_case: UseCase):
        """Return (win, total)"""
        return self.data[user_id][use_case.name]

    def __del__(self):
        with open("db/user_statistics.json", "w") as file:
            json.dump(self.data, file)
