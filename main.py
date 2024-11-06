import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.storage import StateMemoryStorage

import json


token = "UNKNOWN_TOKEN"
with open("token.txt") as file:
    token = file.readline().strip('\n')
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token, state_storage=state_storage, use_class_middlewares=True)

with open("questions.json") as file:
    questions = json.load(file)

class GameStates(StatesGroup):
    gamemode_selecting = State()

class GTLStates(StatesGroup):
    guessing = State()
    answering = State()
    choosing = State()

class HvsAIStates(StatesGroup):
    choosing = State()
    guessing = State()
    answering = State()

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


@bot.message_handler(state=GTLStates.choosing)
def choose_gtl(message, state: StateContext):
    if message.text == "Давай дальше!":
        guess_GTL(message, state)
    elif message.text == "Нет, хватит.":
        state.set(GameStates.gamemode_selecting)
        select_gamemode_message(message, state)

def choose_next_action(message, state: StateContext):
    state.set(GTLStates.choosing)

    btn1 = types.KeyboardButton('Давай дальше!')
    btn2 = types.KeyboardButton('Нет, хватит.')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Ещё одну? 😉", reply_markup=markup)

@bot.message_handler(state=GTLStates.answering)
def answer_gtl(message, state: StateContext):
    user_id = message.from_user.id
    user_state = users_states.get(user_id)

    if user_state == None:
        bot.send_message(user_id, "Что-то пошло не так -_-")
        return
    
    if message.text == user_state["correct_answer"]:
        bot.send_message(user_id, "Верно! 🎉\n" + user_state["question"]["link"] + "\n" + user_state["question"]["author"])
        users_states[user_id] = None

        choose_next_action(message, state)
    else:
        bot.send_message(user_id, "Неверно ¯\_(ツ)_/¯. Попробуй ещё раз.")

def guess_the_level_buttons(message, state: StateContext, question):
    state.set(GTLStates.answering)

    levels = ["Junior", "Middle", "Senior", "Lead"]
    years = ["0-1 years", "1-3 years", "3-6 years", "6+ years"]
    if question["is_level"]:
        buttons = [types.KeyboardButton(level) for level in levels]
    else:
        buttons = [types.KeyboardButton(year) for year in years]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    markup.add(*buttons)
    bot.send_message(message.from_user.id, "Quess the level!", reply_markup=markup)

def guess_GTL(message, state):
    user_id = message.from_user.id
    question_id = get_next_question_id(user_id)
    question = get_question_by_id(question_id)
    if question == None:
        bot.send_message(user_id, "Вопросы закончились 😢")
        
        select_gamemode_message(message, state)
        return

    users_states[user_id] = {
        "question": question,
        "correct_answer": question["level"]
    }

    bot.send_message(message.from_user.id, question["code"])

    guess_the_level_buttons(message, state, question)

def guess_HvsAI(message, state: StateContext):
    bot.send_message(message.from_user.id, "Not implemented yet")
    
    select_gamemode_message(message, state)

@bot.message_handler(state=GameStates.gamemode_selecting)
def gamemode_selecting(message, state: StateContext):
    if message.text == "Guess the Level":
        bot.send_message(message.from_user.id, 'Поехали! 🚀')
        state.set(GTLStates.guessing)
        guess_GTL(message, state)
    elif message.text == "Human vs AI":
        bot.send_message(message.from_user.id, 'Поехали! 🚀')
        state.set(HvsAIStates.guessing)
        guess_HvsAI(message, state)

def select_gamemode_message(message, state: StateContext):
    state.set(GameStates.gamemode_selecting)

    gamemodes = ["Guess the Level", "Human vs AI"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(mode) for mode in gamemodes])
    bot.send_message(message.from_user.id, "Выберите режим игры:", reply_markup=markup)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message, state: StateContext):
    bot.send_message(message.from_user.id, "Добро пожаловать в игру Guess the Something! 🚀\n\n")

    select_gamemode_message(message, state)

bot.add_custom_filter(custom_filters.StateFilter(bot))

from telebot.states.sync.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))

bot.infinity_polling()
