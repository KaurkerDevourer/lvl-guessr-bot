import telebot


token = "UNKNOWN_TOKEN"
with open("token.txt") as file:
    token = file.readline().strip('\n')
bot = telebot.TeleBot(token)

def main():
    print("SUCCESS START")

if __name__ == '__main__':
    main()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

bot.infinity_polling()
