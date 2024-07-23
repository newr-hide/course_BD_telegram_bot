import ast
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import random
from telebot.types import Message

from models import create_tables, Common_word, Word, Program_user

DSN = 'postgresql://postgres:root@localhost:5432/Learning_language'
engine = sqlalchemy.create_engine(DSN)

#Для создания базы данных
#create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
#Для наполнения базы
def insert_words(engine):
    bd_common_words = ((1, 'Мир', 'World'), (2, 'Еда', 'Food'), (3, 'Робот', 'Android'), (4, 'Телефон', 'Phone'), (5, 'Мама', 'Mother'), (6, 'Папа', 'Dad'))

    for id, r_word, en_word in bd_common_words:
        add_word = Common_word(id_common_word=id, russian_word=r_word, english_word=en_word)
        session.add(add_word)

    session.commit()
#insert_words(engine)
#
#Регистрация пользователя в базу данных
def reg_user_(us_id, name):
    list_user = []
    tmp_v = Program_user(id_p_user=us_id, name=name)
    qwery = session.query(Program_user.id_p_user).all()
    if qwery == []:
        session.add(tmp_v)
        session.commit()
    else:
        for i in qwery:
            list_user.append(i[0])
        if us_id in list_user:
            pass
        else:
            print(us_id, name)
            session.add(tmp_v)
            session.commit()
#
def select_word(message):
    global id
    id = message
    select_common_word = session.query(Common_word.russian_word).all()
    select_user_word = session.query(Word.russian_word).filter(Word.id_user == id ).all()
    tmp_list_ = []
    for i in select_common_word:
        tmp_list_.append(i[0].__str__())

    for j in select_user_word:
        tmp_list_.append(j[0].__str__())
   # print(tmp_list)
    tmp_var = random.choice(tmp_list_)
    #print(tmp_var)
    return tmp_var
#select_word()  # Для проверки функции

def select_translite(word):
    result = (session.query(Common_word.english_word).
              filter(Common_word.russian_word == word).all())
    translite = result[0][0]
    return translite
# select_translite('Папа')  # Для проверки функции

def select_other_word(word):
    result_common_word = session.query(Common_word.english_word).filter(Common_word.english_word != word).all()
    result_user_word = session.query(Word.english_word).filter(Word.english_word != word and Word.id_user == id ).all()
    res = result_common_word
    tmp_list =[]
    for i in result_common_word:
        tmp_list.append(i[0].__str__())

    for j in result_user_word:
        tmp_list.append(j[0].__str__())

    random.shuffle(tmp_list)
    #print(tmp_list)
    return tmp_list[0:3]
#select_other_word('Dad')  # Для проверки функции



def add_word(message:Message):
    tmp_list =[]
    global global_temp_rez, id_user_, word_  # заглобалил для использования в функции add_trans_word
    id_user_ = message.from_user.id

    tmp_res = session.query(Word.id_word)
    for i in tmp_res:
        tmp_list.append(int(ast.literal_eval(i.__str__())[0]))
    if not tmp_list:
        global_temp_rez = tmp_list.append(1)
    else:
        global_temp_rez = max(tmp_list) + 1
    word_ = message.text.capitalize()

#add_word('add')  # Для проверки функции

def add_trans_word(message:Message):
    w = message.text.capitalize()
    adding_word = Word(id_user=id_user_, id_word=(global_temp_rez), english_word=word_, russian_word=w)
    session.add(adding_word)
    session.commit()

def delete_word(message:Message):
    tmp_var = message.text
    wrd = tmp_var.capitalize()
    rez = session.query(Word).filter(Word.english_word == wrd).one()
    del_word = rez
    #print(del_word)
    session.delete(del_word)
    session.commit()

session.close()

