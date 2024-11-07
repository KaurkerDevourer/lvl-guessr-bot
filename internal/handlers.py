from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext

from internal import bot
from internal.utils import get_next_question_id, get_data_by_id
from internal.gamemode import Gamemode
from internal.gamemode import pretty_name
from . import user_statistics_storage


class GameStates(StatesGroup):
    gamemode_selecting = State()

class GTLStates(StatesGroup):
    guessing = State()
    answering = State()
    cancel_or_not = State()

class HAIStates(StatesGroup):
    guessing = State()
    answering = State()
    cancel_or_not = State()

users_states = {}

def finish_the_game(message: types.Message, state: StateContext):
    state.delete()
    bot.delete_state(message.from_user.id)
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Спасибо за игру! 🚀", reply_markup=markup)

@bot.message_handler(state="*", commands=["stop"])
def stop_game(message: types.Message, state: StateContext):
    finish_the_game(message, state)

def send_scoreboard_for_mode(message: types.Message, gamemode: Gamemode):
    limit = 20
    scoreboard = user_statistics_storage.GetSorted(gamemode, limit)

    scoreboard_info = ""
    if (scoreboard == None):
        bot.send_message(message.from_user.id, f"Рейтинг {pretty_name(gamemode)} пуст! :(")
        return

    for (username, win, total, rank) in scoreboard:
        if username == message.from_user.username:
            scoreboard_info += f"{rank}. @{username} {win}/{total} <--- Here you are!\n"
            continue
        scoreboard_info += f"{rank}. @{username} {win}/{total}\n"

    bot.send_message(message.from_user.id, f"Топ-{limit} в режиме {pretty_name(gamemode)}:\n{scoreboard_info}")

@bot.message_handler(state="*", commands=['score'])
def send_scoreboard(message: types.Message, state: StateContext):
    send_scoreboard_for_mode(message, Gamemode.GUESS_THE_LVL)
    send_scoreboard_for_mode(message, Gamemode.GUESS_HUMAN_OR_AI)

    select_gamemode_message(message, state)

@bot.message_handler(commands=['score'])
def send_scoreboard_without_session(message: types.Message):
    send_scoreboard_for_mode(message, Gamemode.GUESS_THE_LVL)
    send_scoreboard_for_mode(message, Gamemode.GUESS_HUMAN_OR_AI)

def send_stats_for_mode(message: types.Message, gamemode: Gamemode):
    user_id = message.from_user.id
    username = message.from_user.username

    win, total = user_statistics_storage.Get(username, gamemode)
    rank = user_statistics_storage.GetRank(username, gamemode)

    if rank == None:
        bot.send_message(user_id, f"Ты ещё не сыграл в {pretty_name(gamemode)}!")
        return
    stat_info = f"Твои успехи в {pretty_name(gamemode)}: {win}/{total} (Место в рейтинге: {rank})\n"
    bot.send_message(user_id, stat_info)

@bot.message_handler(state="*", commands=['stats'])
def send_stats(message: types.Message, state: StateContext):
    send_stats_for_mode(message, Gamemode.GUESS_THE_LVL)
    send_stats_for_mode(message, Gamemode.GUESS_HUMAN_OR_AI)

    select_gamemode_message(message, state)

@bot.message_handler(commands=['stats'])
def send_stats_without_session(message: types.Message):
    send_stats_for_mode(message, Gamemode.GUESS_THE_LVL)
    send_stats_for_mode(message, Gamemode.GUESS_HUMAN_OR_AI)

def help_message():
    return "Доступные команды:\n" \
              "/start - начать игру\n" \
              "/stop - завершить игру\n" \
              "/score - показать таблицу лидеров\n" \
              "/stats - показать статистику\n" \
              "/help - показать это сообщение"

@bot.message_handler(state="*", commands=['help'])
def send_help(message: types.Message, state: StateContext):
    bot.send_message(message.from_user.id, help_message())

    select_gamemode_message(message, state)

@bot.message_handler(commands=['help'])
def send_help(message: types.Message):
    bot.send_message(message.from_user.id, help_message())

@bot.message_handler(state=[GTLStates.cancel_or_not, HAIStates.cancel_or_not])
def cancel_or_not(message: types.Message, state: StateContext):
    if message.text == "Нет, хватит.":
        finish_the_game(message, state)
        return

    with state.data() as data:
        gamemode_type = data.get("cancel_or_not")
    if gamemode_type == Gamemode.GUESS_THE_LVL:
        state.set(GTLStates.guessing)
        guess_GTL(message, state)
        return
    
    if gamemode_type == Gamemode.GUESS_HUMAN_OR_AI:
        state.set(HAIStates.guessing)
        guess_HAI(message, state)
        return

    print("WARNING: Unknown state:", state)

def choose_next_action(message: types.Message):
    btn1 = types.KeyboardButton('Давай дальше!')
    btn2 = types.KeyboardButton('Нет, хватит.')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Ещё одну? 😉", reply_markup=markup)

@bot.message_handler(state=GTLStates.answering)
def answer_GTL(message: types.Message, state: StateContext):
    user_id = message.from_user.id
    username = message.from_user.username

    gtl_data = users_states.get(user_id)

    if gtl_data == None:
        print("WARNING: User state is None")
        bot.send_message(user_id, "Что-то пошло не так -_-")
        return

    correct_answer = gtl_data["level"]
    if message.text == correct_answer:
        user_statistics_storage.AddWin(username, Gamemode.GUESS_THE_LVL)
        bot.send_message(user_id, "Верно! 🎉\n")
        users_states[user_id] = None
    else:
        user_statistics_storage.AddFail(username, Gamemode.GUESS_THE_LVL)
        bot.send_message(user_id, r"Неверно ¯\_(ツ)_/¯" + "\n")
        bot.send_message(user_id, f'Правильный ответ: {correct_answer}\n')
    bot.send_message(user_id, f'Пояснение: {gtl_data["solution"]}\n')
    bot.send_message(user_id, f'Ссылка: {gtl_data["link"]}\n')

    choose_next_action(message)
    state.set(GTLStates.cancel_or_not)
    state.add_data(cancel_or_not = Gamemode.GUESS_THE_LVL)

def GTL_guess_buttons(message: types.Message, state: StateContext, question):
    state.set(GTLStates.answering)

    levels = ["Junior", "Middle", "Senior", "Lead"]
    years = ["0-1 years", "1-3 years", "3-6 years", "6+ years"]
    if question["is_level"]:
        buttons = [types.KeyboardButton(level) for level in levels]
    else:
        buttons = [types.KeyboardButton(year) for year in years]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    markup.add(*buttons)
    bot.send_message(message.from_user.id, "Guess the Level!", reply_markup=markup)

def guess_GTL(message: types.Message, state):
    user_id = message.from_user.id
    username = message.from_user.username

    question_id = get_next_question_id(username, Gamemode.GUESS_THE_LVL)
    data = get_data_by_id(question_id, Gamemode.GUESS_THE_LVL)
    if data == None:
        print(f"WARNING: There is no more questions for user: {message.from_user.username}")
        bot.send_message(user_id, "Вы ответили на все вопросы в этом режиме! ✊")
        
        select_gamemode_message(message, state)
        return

    users_states[user_id] = data

    bot.send_message(user_id, '```' + data["lang"] + '\n' + data["code"] + '```', parse_mode='Markdown')

    GTL_guess_buttons(message, state, data)

@bot.message_handler(state=HAIStates.answering)
def answer_HAI(message: types.Message, state: StateContext):
    user_id = message.from_user.id
    username = message.from_user.username

    hai_data = users_states.get(user_id)

    if hai_data == None:
        print("WARNING: User state is None")
        bot.send_message(user_id, "Что-то пошло не так -_-")
        return

    correct_anwer = "Человек" if hai_data["is_human"] else "Бездушная машина 🤖"
    if message.text == correct_anwer:
        user_statistics_storage.AddWin(username, Gamemode.GUESS_HUMAN_OR_AI)
        bot.send_message(user_id, "Верно! 🎉")
        users_states[user_id] = None
    else:
        user_statistics_storage.AddFail(username, Gamemode.GUESS_HUMAN_OR_AI)
        bot.send_message(user_id, r"Неверно ¯\_(ツ)_/¯" + "\n")

    choose_next_action(message)
    state.set(HAIStates.cancel_or_not)
    state.add_data(cancel_or_not = Gamemode.GUESS_HUMAN_OR_AI)

def HAI_guess_buttons(message: types.Message, state: StateContext):
    state.set(HAIStates.answering)

    candidates = ["Человек", "Бездушная машина 🤖"]
    buttons = [types.KeyboardButton(candidate) for candidate in candidates]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    markup.add(*buttons)

    bot.send_message(message.from_user.id, "Угадай, человек или ИИ написал этот код?", reply_markup=markup)

def guess_HAI(message: types.Message, state: StateContext):
    user_id = message.from_user.id
    username = message.from_user.username

    question_id = get_next_question_id(username, Gamemode.GUESS_HUMAN_OR_AI)
    data = get_data_by_id(question_id, Gamemode.GUESS_HUMAN_OR_AI)
    if data == None:
        print(f"WARNING: There is no more questions for user: {message.from_user.username}")
        bot.send_message(user_id, "Вы ответили на все вопросы в этом режиме! ✊")

        select_gamemode_message(message, state)
        return

    bot.send_message(user_id, '```' + data["lang"] + '\n' + data["code"] + '```', parse_mode='Markdown')

    users_states[user_id] = data

    HAI_guess_buttons(message, state)

@bot.message_handler(state=GameStates.gamemode_selecting)
def gamemode_selecting(message: types.Message, state: StateContext):
    if message.text == pretty_name(Gamemode.GUESS_THE_LVL):
        bot.send_message(message.from_user.id, 'Поехали! 🚀')
        state.set(GTLStates.guessing)
        guess_GTL(message, state)
    elif message.text == pretty_name(Gamemode.GUESS_HUMAN_OR_AI):
        bot.send_message(message.from_user.id, 'Поехали! 🚀')
        state.set(HAIStates.guessing)
        guess_HAI(message, state)

def select_gamemode_message(message: types.Message, state: StateContext):
    state.set(GameStates.gamemode_selecting)

    gamemodes = [pretty_name(gamemode) for gamemode in Gamemode]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(mode) for mode in gamemodes])
    bot.send_message(message.from_user.id, "Выберите режим игры:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message, state: StateContext):
    bot.send_message(message.from_user.id, "Добро пожаловать в игру Guess the Something! 🚀\n\n")

    select_gamemode_message(message, state)
