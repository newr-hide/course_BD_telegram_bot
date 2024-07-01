import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from  models import English_word, Russian_word, Bridge_russ_en_word
import random

DSN = 'postgresql://postgres:root@localhost:5432/Learning_language'
engine = sqlalchemy.create_engine(DSN)




Session = sessionmaker(bind=engine)
session = Session()


def select_word():
    tmp = session.query(English_word).all()
    tmp_list = []
    for i in tmp:
        word_search = i.__str__()
        tmp_list.append(word_search)
        random_choise = random.choice(tmp_list)
    return random_choise


def select_translite(word):
    result = (session.query(Russian_word).select_from(Bridge_russ_en_word).filter(English_word.word == word).
              join(English_word, Bridge_russ_en_word.id_english_word == English_word.id_english_word).
              join(Russian_word, Bridge_russ_en_word.id_russian_word == Russian_word.id_russian_word).all())

    translite = result[0]
    return translite

def select_other_word(word):
    result = session.query(English_word).filter(English_word.word != word).all()
    tmp_list =[]
    for i in result:
        tmp_list.append(i.__str__())

    return tmp_list[0:3]

def insert_word():
    word = input('Какое слово хотите добавить на английском языке?')
    result = session.add(word)
    session.commit()

session.close()

