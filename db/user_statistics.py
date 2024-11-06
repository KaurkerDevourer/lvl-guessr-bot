import json
from collections import defaultdict
import os

from internal.gamemode import Gamemode

class UserStatisticsStorage:
    def __init__(self, file_name: str = "db/user_statistics.json"):
        self.file_name = file_name
        self.data = defaultdict(lambda: defaultdict(lambda: (0, 0)))
        if not os.path.exists(self.file_name):
           print(f"ERROR: File '{self.file_name}' not found")
           return
        
        with open(self.file_name, "r") as file:
            raw_data = json.loads(file.read())

        for (user_id, stat) in raw_data.items():
            self.data[user_id] = defaultdict(lambda: (0, 0), tuple(stat.items()))

    def Serialize(self):
        s = json.dumps(self.data)
        with open(self.file_name, "w") as file:
            file.write(s)

    def AddWin(self, user_id: str, gamemode: Gamemode):
        (win, total) = self.data[user_id][gamemode.name]
        self.data[user_id][gamemode.name] = (win + 1, total + 1)
        self.Serialize()

    def AddFail(self, user_id: str, gamemode: Gamemode):
        (win, total) = self.data[user_id][gamemode.name]
        self.data[user_id][gamemode.name] = (win, total + 1)
        self.Serialize()

    def Get(self, user_id: str, gamemode: Gamemode):
        """Return (win, total)"""
        return self.data[user_id][gamemode.name]

    def GetRank(self, user_id: str, gamemode: Gamemode):
        """Return rank"""
        # TODO: nth_element
        sorted_data = sorted(self.data.items(), key=lambda x: x[1][gamemode.name][0], reverse=True)
        for rank, (user_id, _) in enumerate(sorted_data, 1):
            if user_id == user_id:
                return rank
        return None

    def GetSorted(self, gamemode: Gamemode, limit: int = 20):
        """Return list of tuples (user_id, (win, total, rank)) sorted by win"""
        if limit <= 0:
            print(f"ERROR: Limit (which is {limit}) must be positive")
            return None

        if limit > len(self.data):
            limit = len(self.data)

        win_idx = 0
        sorted_data = sorted(self.data.items(), key=lambda x: x[1][gamemode.name][win_idx], reverse=True)[:limit]

        result = []
        for rank, (user_id, data) in enumerate(sorted_data, 1):
            win, total = data[gamemode.name]
            result.append((user_id, (win, total, rank)))
        return result if len(result) > 0 else None

