import telebot
import db

TOKEN = "681428134:AAFidZQVN2NIa_FFZlItvgHEsRjMjEQQ76I"
DATABASE = "VoiceDB.db"

if __name__ == "__main__":
    bot = telebot.TeleBot(TOKEN)
    db = db.VoiceDB(DATABASE)
    users = db.get_users()

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(content_types=['voice'])
    def handle_docs_voice(message):
        try:
            uid = message.chat.id
            if uid not in users:
                db.add_user(uid, message.chat.username)
                users.append(uid)

            file_info = bot.get_file(message.voice.file_id)
            voice = bot.download_file(file_info.file_path)
            db.write_voice(uid, voice)

            bot.reply_to(message, "Аудио сообщение добавлено")
        except Exception as e:
            bot.reply_to(message, e)

    bot.polling(none_stop=False, interval=0, timeout=20)
