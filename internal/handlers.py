from internal import bot
from internal.utils import get_next_question_id, get_question_by_id
from telebot import types

users_states = {}

@bot.message_handler(commands=['guess'])
def start_the_game(message):
    bot.send_message(message.from_user.id, 'Поехали! 🚀')

    user_id = message.from_user.id
    question_id = get_next_question_id(user_id)
    question = get_question_by_id(question_id)
    if question is None:
        bot.send_message(user_id, "Вопросы закончились 😢")
        return

    users_states[user_id] = {
        "question": question,
        "correct_answer": question["level"]
    }

    bot.send_message(message.from_user.id, question["code"])

    # TODO: возможно, можно создать 1 раз и переиспользовать
    if question["is_level"]:
        btn1 = types.KeyboardButton('Junior')
        btn2 = types.KeyboardButton('Middle')
        btn3 = types.KeyboardButton('Senior')
    else:
        btn1 = types.KeyboardButton('0-1 years')
        btn2 = types.KeyboardButton('1-3 years')
        btn3 = types.KeyboardButton('3-6 years')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, "Quess the level!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def on_message_create(message):

    user_id = message.from_user.id
    state = users_states.get(user_id)

    if state:
        if message.text == state["correct_answer"]:
            bot.send_message(user_id, "Да! 🎉\n" + state["question"]["link"] + "\n" + state["question"]["author"])
            users_states[user_id] = None
        else:
            bot.send_message(user_id, "Неправильно. Попробуй ещё раз.")
    else:
        bot.send_message(user_id, "Начни игру, используя команду /guess.")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Добро пожаловать в игру Guess the Level! 🚀\n\n")
    bot.send_message(message.from_user.id, "Чтобы начать, наберите /guess")