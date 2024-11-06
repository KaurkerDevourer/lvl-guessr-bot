import internal.handlers
from internal import bot
from telebot import custom_filters
from telebot.states.sync.middleware import StateMiddleware

def main():
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.setup_middleware(StateMiddleware(bot))
    bot.infinity_polling()

if __name__ == '__main__':
    main()
