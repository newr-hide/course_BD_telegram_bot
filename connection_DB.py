import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from  models import English_word, Russian_word, Bridge_russ_en_word
import random

DSN = 'postgresql://postgres:root@localhost:5432/Learning_language'
engine = sqlalchemy.create_engine(DSN)

def select_word():
    tmp = session.query(English_word).all()
    tmp_list = []
    for i in tmp:
        word_search = i.__str__()
        tmp_list.append(word_search)
        random_choise = random.choice(tmp_list)
    return random_choise


def select_translite():
    tmp = session.query(Russian_word)

Session = sessionmaker(bind=engine)
session = Session()

session.close()
select_word()