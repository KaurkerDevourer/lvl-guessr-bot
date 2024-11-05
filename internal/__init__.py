import telebot
import json

with open("token.txt") as file:
    token = file.readline().strip('\n')
bot = telebot.TeleBot(token)

with open("db/questions.json") as file:
    questions = json.load(file)