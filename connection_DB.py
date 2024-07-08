import ast

import telebot
import sqlalchemy
from sqlalchemy.orm import sessionmaker


from  models import English_word, Russian_word, create_tables, Program_user
import random
from telebot.types import Message
DSN = 'postgresql://postgres:root@localhost:5432/Learning_language'
engine = sqlalchemy.create_engine(DSN)

# create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

def reg_user_(user_id, name):
    tmp_v = Program_user(id_p_user=user_id,name=name)
    qwery = session.query(Program_user.id_p_user).all()
    for i in qwery:
        if i[0] == user_id:
            pass
        else:
            session.add(tmp_v)
            session.commit()

def select_word():
    tmp = session.query(English_word).all()
    tmp_list = []
    for i in tmp:
        tmp_list.append(i.__str__())
    tmp_var = random.choice(tmp_list)
    return tmp_var


def select_translite(word):
    result = (session.query(Russian_word).join(English_word, English_word.id_english_word == Russian_word.id_en_word).
              filter(English_word.word == word).with_entities(Russian_word.word).all())
    translite = result[0][0]
    print(translite)
    return translite


def select_other_word(word):
    result = session.query(English_word).filter(English_word.word != word).all()
    tmp_list =[]
    for i in result:
        tmp_list.append(i.__str__())
    return tmp_list[0:3]
def add_word(message:Message):
    tmp_list =[]
    tmp_res = session.query(English_word.id_english_word)
    for i in tmp_res:
        tmp_list.append(int(ast.literal_eval(i.__str__())[0]))
    global global_temp_rez # заглобалил для использования в функции add_trans_word
    global_temp_rez = max(tmp_list)
    w = message.text
    wd = English_word(word=w,id_english_word=global_temp_rez+1)
    session.add(wd)
    session.commit()

def add_trans_word(message:Message):
    tmp_list = []
    tmp_res = session.query(Russian_word.id_russian_word)
    for i in tmp_res:
        tmp_list.append(i.__str__())
    tmp_rez = max(tmp_list)
    temp_rez2 = int(ast.literal_eval(tmp_rez)[0])
    w = message.text
    word = Russian_word( word=w, id_russian_word=temp_rez2+1, id_en_word=global_temp_rez+1)
    session.add(word)
    session.commit()

def delete_word(message:Message):
    tmp_var = message.text
    wrd = tmp_var.capitalize()
    rez = session.query(English_word).filter(English_word.word == wrd).one()
    session.delete(rez)
    session.commit()





session.close()

