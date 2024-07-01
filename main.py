import telebot
from telebot import types
from telebot.handler_backends import StatesGroup, State
import random
from connection_DB import select_word


TOKEN = '7390295624:AAEUlfl4o-cpZNqSEvarnJlK24OUP_ZCIIA'
bot = telebot.TeleBot(TOKEN)

class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'

class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()

import_func = select_word()

@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)

    russian_word = import_func

    english_word = 'Peace'
    english_word_btn = types.KeyboardButton(english_word)
    other_word = ['Car','Hello','Dad']
    other_word_btn = [types.KeyboardButton(word) for word in other_word]
    buttons = [english_word_btn] + other_word_btn
    random.shuffle(buttons)

    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])
    markup.add(*buttons)
    bot.send_message(message.chat.id, f'Как переводится слово {russian_word}',reply_markup=markup)

    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['english_word'] = english_word
        data['russian_word'] = russian_word
        data['other_words'] = other_word

@bot.message_handler(func=lambda message: True, content_types=['text'])

def message_reply(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        english_word = data['english_word']
    if message.text == english_word:
        bot.send_message(message.chat.id, 'Все верно')
    else:
        bot.send_message(message.chat.id, 'Неверно')



@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.send_message(message.chat.id,"ADD word - Добавляет новое слово в словарь\n"
                                 "DELETE word - удаляет слово из словаря\n"
                                 "NEXT - следующее слово\n"
                                 "WORDS FOR THE DAY - слова для запоминания на день\n")


if __name__ == '__main__':
    print("Бот запущен")
    bot.polling()