import json
from enum import Enum
from collections import defaultdict
import os


class UseCase(Enum):
    GUESS_THE_LVL = 0
    AI_VS_HUMAN = 1


class UserStatisticsStorage:
    def __init__(self, file_name: str = "db/user_statistics.json"):
        self.file_name = file_name
        self.data = defaultdict(lambda: defaultdict(lambda: (0, 0)))
        if not os.path.exists(self.file_name):
           return
        
        with open(self.file_name, "r") as file:
            raw_data = json.loads(file.read())

        for (user_id, stat) in raw_data.items():
            self.data[user_id] = defaultdict(lambda: (0, 0), stat)
            
    def Serialize(self):
        s = json.dumps(self.data)
        with open(self.file_name, "w") as file:
            file.write(s)

    def AddWin(self, user_id: str, use_case: UseCase):
        """Example of a call: stat.add_win("user_id", UseCase.GUESS_THE_LVL)"""
        (win, total) = self.data[user_id][use_case.name]
        self.data[user_id][use_case.name] = (win + 1, total + 1)
        self.Serialize()

    def AddFail(self, user_id: str, use_case: UseCase):
        (win, total) = self.data[user_id][use_case.name]
        self.data[user_id][use_case.name] = (win, total + 1)
        self.Serialize()

    def Get(self, user_id: str, use_case: UseCase):
        """Return (win, total)"""
        return self.data[user_id][use_case.name]
