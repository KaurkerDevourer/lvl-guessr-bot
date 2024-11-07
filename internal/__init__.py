import telebot
from telebot.storage import StateMemoryStorage

from db.challenge_db_handler import ChallengeStorage
from db.user_statistics import UserStatisticsStorage

import json

with open("token.txt") as file:
    token = file.readline().strip('\n')
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token, state_storage=state_storage, use_class_middlewares=True)

with open("db/questions.json") as file:
    questions = json.load(file)

with open("db/hai/hai_db.json") as file:
    hai_db = json.load(file)

user_statistics_storage = UserStatisticsStorage()
challenge_storage = ChallengeStorage()
