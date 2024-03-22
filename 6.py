import telebot
from telebot import types
import config # Импорт config.py
import urllib.request # request нужен для загрузки файлов от пользователя
import os

token = config.BOT_TOKEN
bot = telebot.TeleBot(token)

# Функция получения списка файлов с расширениями '.xlsx', '.xls', '.odt'
def get_folder_files(folder):
    files = []
    files += [each for each in os.listdir(folder) if each.endswith('.xlsx') or each.endswith('.xls') or each.endswith('.odt')]
    return files

# Функция start
@bot.message_handler(commands=['start'])
def hello(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    files = get_folder_files(config.folder)
    # files_item: object
    for files_item in files:
        first_symbol = str(files_item)
        first_symbol = first_symbol[0]
        # Временные файлы не игнорируем
        if first_symbol != '~':
            keyboard.add(types.KeyboardButton(files_item))
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, ты можешь скачать следующие файлы:', reply_markup=keyboard)

# Функция, обрабатывающая команду /info
@bot.message_handler(commands=['info'])
def welcome_help(message):
    bot.send_message(message.chat.id, 'Этот бот предназначен для обмена файлами с сервисом')

# Функция получения табличного файла
@bot.message_handler(content_types=['text'])
def main_menu(message):
    files = get_folder_files(config.folder)
    # files_item: object
    for files_item in files:
        if message.text == files_item:
            first_symbol = files_item[0]
            # Временные файлы не игнорируем
            if first_symbol != '~':
                # формируем полный путь к файлу
                full_files_item = config.folder + os.sep + files_item
                f = open(full_files_item, 'rb')
                # bot.send_document(message.chat.id, document=f, caption=files_item)
                bot.send_document(message.chat.id, document=f)
            break

# Заготовка функции отправки файла на сервер
@bot.message_handler(content_types=["document"])
def handle_docs(message):
    bot.send_message(message.chat.id, message.text)
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{config.BOT_TOKEN}/{file_info.file_path}', file_info.file_path)
    newFile = message.effective_attachment.get_file()
    newFile.download('file_name')

# Запуск бота
bot.polling(none_stop=True)