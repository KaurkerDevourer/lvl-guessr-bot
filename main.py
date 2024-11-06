import telebot
from telebot import types

import json

token = "UNKNOWN_TOKEN"
with open("token.txt") as file:
    token = file.readline().strip('\n')
bot = telebot.TeleBot(token)

with open("questions.json") as file:
    questions = json.load(file)


users_states = {}

def get_next_question_id(user_id) -> int:
    # TODO: запрашиваем информацию из БД или файла
    return 0

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

@bot.message_handler(commands=['guess'])
def start_the_game(message):
    bot.send_message(message.from_user.id, 'Поехали! 🚀')

    user_id = message.from_user.id
    question_id = get_next_question_id(user_id)
    question = get_question_by_id(question_id)
    if question == None:
        bot.send_message(user_id, "Вопросы закончились 😢")
        return

    users_states[user_id] = {
        "question": question,
        "correct_answer": question["level"]
    }

    bot.send_message(message.from_user.id, question["code"])

    levels = ["Junior", "Middle", "Senior", "Lead"]
    years = ["0-1 years", "1-3 years", "3-6 years", "6+ years"]
    if question["is_level"]:
        buttons = [types.KeyboardButton(level) for level in levels]
    else:
        buttons = [types.KeyboardButton(year) for year in years]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    markup.add(*buttons)
    bot.send_message(message.from_user.id, "Quess the level!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def on_message_create(message):

    user_id = message.from_user.id
    state = users_states.get(user_id)

    if state:
        if message.text == state["correct_answer"]:
            bot.send_message(user_id, "Верно! 🎉\n" + state["question"]["link"] + "\n" + state["question"]["author"])
            users_states[user_id] = None
        else:
            bot.send_message(user_id, "Неверно ¯\_(ツ)_/¯. Попробуй ещё раз.")
    else:
        bot.send_message(user_id, "Начни игру, используя команду /guess.")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Добро пожаловать в игру Guess the Level! 🚀\n\n")
    bot.send_message(message.from_user.id, "Чтобы начать, наберите /guess")

bot.infinity_polling()
