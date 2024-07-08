import telebot
from telebot import types
from telebot.types import Message
from telebot.handler_backends import StatesGroup, State
import random
from connection_DB import  add_word, delete_word,add_trans_word,select_word, select_translite, select_other_word,reg_user_

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

userStep = {}
known_users = []
buttons = []
# def show_hint(*lines):
#     return '\n'.join(lines)
# def show_target(data):
#     return f"{data['english_word']} -> {data['russian_word']}"
# def get_user_step(uid):
#     if uid in userStep:
#         return userStep[uid]
#     else:
#         known_users.append(uid)
#         userStep[uid] = 0
#         print("New user detected, who hasn't used \"/start\" yet")
#         return 0

class Command:

    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'

class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()


@bot.message_handler(commands=['start'])

def start_bot(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    reg_user_(user_id, user_name)
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    target_word = select_word()
    russian_word = select_translite(target_word)
    english_word_btn = types.KeyboardButton(target_word)
    other_word = select_other_word(target_word)
    other_word_btn = [types.KeyboardButton(word) for word in other_word]
    btns = [english_word_btn] + other_word_btn
    random.shuffle(buttons)

    next_btn = types.KeyboardButton(Command.NEXT)

    add_word_btn = types.KeyboardButton(Command.ADD_WORD)

    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    btns.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*btns)
    bot.send_message(message.chat.id, f'Как переводится слово {russian_word}',reply_markup=markup)

    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['russian_word'] = russian_word
        data['other_words'] = other_word

@bot.message_handler(func=lambda message: message.text == Command.NEXT) # Работа кнопки следущее
def next(message):
    start_bot(message)
@bot.message_handler(func=lambda command: command.text == Command.ADD_WORD) # Работа кнопки вставить слово
def add(message:Message):
    bot.send_message(message.chat.id, 'Введите какое слово на английском языке добавить?')
    bot.register_next_step_handler(message,add_word)
    bot.register_next_step_handler(message, add_trans)
def add_trans(message):
    bot.send_message(message.chat.id, 'Введите перевод слова')
    bot.register_next_step_handler(message, add_trans_word)


@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def del_word(message:Message):
    bot.send_message(message.chat.id, 'Какое слово на английском языке Вы хотите удалить?')
    bot.register_next_step_handler(message, delete_word)



@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.send_message(message.chat.id,"ADD word - Добавляет новое слово в словарь\n"
                                 "DELETE word - удаляет слово из словаря\n"
                                 "NEXT - следующее слово\n"
                                 "WORDS FOR THE DAY - слова для запоминания на день\n")

@bot.message_handler(func=lambda message: True, content_types=['text'])

def message_reply(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

        target_word = data['target_word']
    if message.text == target_word:
        bot.send_message(message.chat.id, 'Все верно')
    else:
        bot.send_message(message.chat.id, 'Неверно')




if __name__ == '__main__':
    print("Бот запущен")
    bot.polling()