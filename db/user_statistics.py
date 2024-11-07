import json
from collections import defaultdict
import os
import sqlite3

from internal.gamemode import Gamemode

class UserStatisticsStorage:
    def __init__(self, file_name: str = "db/user_statistics.db"):
        self.connection = sqlite3.connect(file_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS user_statistics (user_id TEXT, gamemode TEXT, win INTEGER, total INTEGER, UNIQUE(user_id, gamemode))")
        self.connection.commit()

    def Serialize(self):
        s = json.dumps(self.data)
        with open(self.file_name, "w") as file:
            file.write(s)

    def AddWin(self, user_id: str, gamemode: Gamemode):
        self.cursor.execute(
            "INSERT INTO user_statistics(user_id, gamemode, win, total) "
            "VALUES (?, ?, 1, 1) "
            "ON CONFLICT(user_id, gamemode) DO "
            "UPDATE SET win = win + 1, total = total + 1 "
            "WHERE user_id = ? AND gamemode = ? ", (user_id, gamemode.name, user_id, gamemode.name))
        self.connection.commit()

    def AddFail(self, user_id: str, gamemode: Gamemode):
        self.cursor.execute(
            "INSERT INTO user_statistics(user_id, gamemode, win, total) "
            "VALUES (?, ?, 0, 1) "
            "ON CONFLICT(user_id, gamemode) DO "
            "UPDATE SET total = total + 1 "
            "WHERE user_id = ? AND gamemode = ? ", (user_id, gamemode.name, user_id, gamemode.name))
        self.connection.commit()

    def Get(self, user_id: str, gamemode: Gamemode):
        """Return (win, total)"""
        self.cursor.execute("SELECT win, total FROM user_statistics WHERE user_id = ? AND gamemode = ?", (user_id, gamemode.name))
        result = self.cursor.fetchone()
        return result if result is not None else (0, 0)

    def GetRank(self, user_id: str, gamemode: Gamemode):
        """Return rank"""
        self.cursor.execute(
            "SELECT user_id, RANK() OVER (ORDER BY win DESC) AS rank "
            "FROM user_statistics "
            "WHERE gamemode = ? ", (gamemode.name,))

        for rank, (user_id, rank) in enumerate(self.cursor.fetchall(), 1):
            if user_id == user_id:
                return rank
        return None

    def GetSorted(self, gamemode: Gamemode, limit: int = 20):
        """Return list of tuples (user_id, win, total, rank) sorted by win"""
        if limit <= 0:
            print(f"ERROR: Limit (which is {limit}) must be positive")
            return None

        self.cursor.execute(
            "SELECT user_id, win, total, RANK() OVER (ORDER BY win DESC) AS rank "
            "FROM user_statistics "
            "WHERE gamemode = ? "
            "LIMIT ? ", (gamemode.name, limit))
        
        return self.cursor.fetchall()

