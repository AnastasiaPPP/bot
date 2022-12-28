import telebot
from telebot import types
import weather_pars
import adding_new_entry
import os.path
import data_transformation as d_t
import pathlib

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    names = f'Привет, {message.from_user.first_name}!'
    bot.send_message(message.chat.id, names)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    nb = types.KeyboardButton("Записная книжка")
    weath = types.KeyboardButton("Погода в Екатеринбурге")
    markup.add(nb, weath)
    bot.send_message(message.chat.id, 'Нажмите кнопку', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def get_mes(msg):
    if msg.text == "Погода в Екатеринбурге":
        weather = weather_pars.show_weather()
        bot.send_message(msg.chat.id, weather)
    elif msg.text == "Записная книжка":
        menu =  "1. Посмотреть записи \n 2. Добавить новую запись \n 3. Импорт данных \n 4. Экспорт данных"
        bot.send_message(msg.chat.id, menu)
    elif msg.text == "1":
        txt = adding_new_entry.show_data()
        for i in txt:
            bot.send_message(msg.chat.id, i)
        bot.send_message(msg.chat.id, 'Для выхода в меню нажмите любую букву')
    elif msg.text == "2":
        message = bot.send_message(msg.chat.id, 'Введите день, время и событие в одну строку')
        bot.register_next_step_handler(message, start_2)
    elif msg.text == "3":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        f1 = types.KeyboardButton(".txt")
        f2 = types.KeyboardButton(".scv")
        markup.add(f1, f2)
        mess = bot.send_message(msg.chat.id, 'Выберите формат для импорта', reply_markup=markup)
        bot.register_next_step_handler(mess, handl_button)
    elif msg.text == "4":
        bot.send_message(msg.chat.id, 'Загрузите файл')
    else:
        start(msg)
        


@bot.message_handler(content_types=['document'])
def handle_doc(message):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        path = pathlib.Path.cwd()
        save_path = os.path.join(path, message.document.file_name)
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        sticker="https://github.com/TelegramBots/book/raw/master/src/docs/sticker-fred.webp"
        bot.send_message(message.chat.id, "Пожалуй, сохраню \n Чтобы вернуться в меню нажмите любую букву")
        bot.send_sticker(message.chat.id, sticker) 


def handl_button(msg):
    if msg.text == ".txt":
        dir_path = pathlib.Path.cwd()
        path = pathlib.Path(dir_path, 'data_file.txt')
        file = open(path, 'r', encoding='utf-8')
        bot.send_document(msg.chat.id, file)
        bot.send_message(msg.chat.id, 'Чтобы вернуться в меню нажмите любую букву')
    elif msg.text == ".scv":
        d_t.converting_to_csv()
        dir_path = pathlib.Path.cwd()
        path = pathlib.Path(dir_path, 'data_file.scv')
        file = open(path, 'r', encoding='utf-8')
        bot.send_document(msg.chat.id, file)
        bot.send_message(msg.chat.id, 'Чтобы вернуться в меню нажмите любую букву')


def start_2(message):
    adding_new_entry.new_entry(message.text)
    bot.send_message(message.chat.id, 'Готово! \n Чтобы вернуться в меню нажмите любую букву')


bot.polling(none_stop=True)
