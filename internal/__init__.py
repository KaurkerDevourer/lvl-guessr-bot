import telebot
from telebot.storage import StateMemoryStorage

import json

with open("token.txt") as file:
    token = file.readline().strip('\n')
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token, state_storage=state_storage, use_class_middlewares=True)

with open("db/questions.json") as file:
    questions = json.load(file)
