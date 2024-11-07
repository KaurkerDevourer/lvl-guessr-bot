import json
from collections import defaultdict
import os
import sqlite3

from internal.gamemode import Gamemode

class UserStatisticsStorage:
    def __init__(self, file_name: str = "db/user_statistics.db"):
        self.connection = sqlite3.connect(file_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS user_statistics (username TEXT, gamemode TEXT, win INTEGER, total INTEGER, UNIQUE(username, gamemode))")
        self.connection.commit()

    def AddWin(self, username: str, gamemode: Gamemode):
        self.cursor.execute(
            "INSERT INTO user_statistics(username, gamemode, win, total) "
            "VALUES (?, ?, 1, 1) "
            "ON CONFLICT(username, gamemode) DO "
            "UPDATE SET win = win + 1, total = total + 1 "
            "WHERE username = ? AND gamemode = ? ", (username, gamemode.name, username, gamemode.name))
        self.connection.commit()

    def AddFail(self, username: str, gamemode: Gamemode):
        self.cursor.execute(
            "INSERT INTO user_statistics(username, gamemode, win, total) "
            "VALUES (?, ?, 0, 1) "
            "ON CONFLICT(username, gamemode) DO "
            "UPDATE SET total = total + 1 "
            "WHERE username = ? AND gamemode = ? ", (username, gamemode.name, username, gamemode.name))
        self.connection.commit()

    def Get(self, username: str, gamemode: Gamemode):
        """Return (win, total)"""
        self.cursor.execute("SELECT win, total FROM user_statistics WHERE username = ? AND gamemode = ?", (username, gamemode.name))
        result = self.cursor.fetchone()
        if result is None:
            print(f"WARNING: There is no data for {username} in {gamemode}")
            return (0, 0)
        return result

    def GetRank(self, username: str, gamemode: Gamemode):
        """Return rank"""
        self.cursor.execute(
            "SELECT username, RANK() OVER (ORDER BY win DESC) AS rank "
            "FROM user_statistics "
            "WHERE gamemode = ? ", (gamemode.name,))

        for rank, (username, rank) in enumerate(self.cursor.fetchall(), 1):
            if username == username:
                return rank
        return None

    def GetSorted(self, gamemode: Gamemode, limit: int = 20):
        """Return list of tuples (username, win, total, rank) sorted by win"""
        if limit <= 0:
            print(f"ERROR: Limit (which is {limit}) must be positive")
            return None

        self.cursor.execute(
            "SELECT username, win, total, RANK() OVER (ORDER BY win DESC) AS rank "
            "FROM user_statistics "
            "WHERE gamemode = ? "
            "LIMIT ? ", (gamemode.name, limit))
        
        return self.cursor.fetchall()
