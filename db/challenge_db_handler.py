import json
import sqlite3


class ChallengeStorage:
    def __init__(self, file_name: str = "db/challenges.db"):
        self.connection = sqlite3.connect(file_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

        # Create the challengeDb table with an auto-incrementing challengeId
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS challengeDb ("
            "challengeId INTEGER PRIMARY KEY AUTOINCREMENT, "
            "questionIds TEXT, "
            "isFinished INTEGER DEFAULT 0)"
        )

        # Create the challengeResults table for storing challenge results
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS challengeResults ("
            "challengeId INTEGER, "
            "userId TEXT, "
            "result INTEGER, "
            "UNIQUE(challengeId, userId))"
        )

        self.connection.commit()

    def AddChallenge(self, questionIds: list, isFinished: bool = False):
        """Adds a new challenge with a list of question IDs and finished status."""
        questionIds_str = json.dumps(questionIds)
        self.cursor.execute(
            "INSERT INTO challengeDb (questionIds, isFinished) VALUES (?, ?)",
            (questionIds_str, int(isFinished))
        )
        self.connection.commit()

        # Return the auto-incremented challengeId of the new row
        return self.cursor.lastrowid

    def UpdateChallenge(self, challengeId: int, questionIds: list = None, isFinished: bool = None):
        """Updates question IDs or finished status for a specific challenge."""
        if questionIds is not None:
            questionIds_str = json.dumps(questionIds)
            self.cursor.execute("UPDATE challengeDb SET questionIds = ? WHERE challengeId = ?",
                                (questionIds_str, challengeId))
        if isFinished is not None:
            self.cursor.execute("UPDATE challengeDb SET isFinished = ? WHERE challengeId = ?",
                                (int(isFinished), challengeId))
        self.connection.commit()

    def GetChallenge(self, challengeId: int):
        """Returns challenge details (challengeId, questionIds, isFinished)."""
        self.cursor.execute("SELECT challengeId, questionIds, isFinished FROM challengeDb WHERE challengeId = ?",
                            (challengeId,))
        result = self.cursor.fetchone()
        if result:
            challengeId, questionIds_str, isFinished = result
            questionIds = json.loads(questionIds_str)
            return (challengeId, questionIds, bool(isFinished))
        return None

    def DeleteChallenge(self, challengeId: int):
        """Deletes a specific challenge."""
        self.cursor.execute("DELETE FROM challengeDb WHERE challengeId = ?", (challengeId,))
        self.connection.commit()

    def AddChallengeResult(self, challengeId: int, userId: str, result: int):
        """Adds or updates a result for a specific challenge and user."""
        self.cursor.execute(
            "INSERT OR REPLACE INTO challengeResults (challengeId, userId, result) "
            "VALUES (?, ?, ?)",
            (challengeId, userId, result)
        )
        self.connection.commit()

    def GetChallengeResult(self, challengeId: int, userId: str):
        """Returns the result for a specific challenge and user."""
        self.cursor.execute("SELECT result FROM challengeResults WHERE challengeId = ? AND userId = ?",
                            (challengeId, userId))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def GetChallengeResultsByChallengeId(self, challengeId: int):
        self.cursor.execute("SELECT result, userId FROM challengeResults WHERE challengeId = ?", (challengeId,))
        results = self.cursor.fetchall()

        if results:
            return results
        return None


    def UpdateChallengeResult(self, challengeId: int, userId: str, result: int):
        """Updates the result for a specific challenge and user."""
        self.cursor.execute(
            "UPDATE challengeResults SET result = ? WHERE challengeId = ? AND userId = ?",
            (result, challengeId, userId)
        )
        self.connection.commit()

    def DeleteChallengeResult(self, challengeId: int, userId: str):
        """Deletes a specific user's result for a challenge."""
        self.cursor.execute("DELETE FROM challengeResults WHERE challengeId = ? AND userId = ?", (challengeId, userId))
        self.connection.commit()

    def GetResultsForChallenge(self, challengeId: int):
        """Returns a list of all results for a specific challenge."""
        self.cursor.execute("SELECT userId, result FROM challengeResults WHERE challengeId = ?", (challengeId,))
        return self.cursor.fetchall()

    def GetAllChallenges(self, limit: int = 20):
        """Returns a list of challenges with their details, limited by a specified number."""
        self.cursor.execute("SELECT challengeId, questionIds, isFinished FROM challengeDb LIMIT ?", (limit,))
        results = self.cursor.fetchall()
        return [(cid, json.loads(qids), bool(finished)) for cid, qids, finished in results]
