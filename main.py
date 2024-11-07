import internal.handlers
from internal import bot
from telebot import custom_filters, types
from telebot.states.sync.middleware import StateMiddleware

commands = [
    types.BotCommand("start", "Начать игру"),
    types.BotCommand("stop", "Завершить игру"),
    types.BotCommand("stats", "Показать личную статистику"),
    types.BotCommand("score", "Показать топ игроков")
]

def main():
    bot.set_my_commands(commands)
    bot.add_custom_filter(custom_filters.StateFilter(bot))

    bot.setup_middleware(StateMiddleware(bot))
    bot.infinity_polling()

if __name__ == '__main__':
    main()
