import telebot

TOKEN = "681428134:AAFidZQVN2NIa_FFZlItvgHEsRjMjEQQ76I"

if __name__ == "__main__":
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")

    bot.polling(none_stop=False, interval=0, timeout=20)
