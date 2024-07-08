import sqlalchemy as alh
from sqlalchemy import PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship, declared_attr, declarative_base


Base = declarative_base()

class Program_user(Base):
    __tablename__ = "program_user"

    id_p_user = alh.Column(alh.Integer, primary_key=True)
    name = alh.Column(alh.String(length=60), unique=True)

    def __str__(self):
        return f'{self.name}'

class Russian_word(Base):
    __tablename__ = "russian_word"

    id_russian_word = alh.Column(alh.Integer, primary_key=True)
    word = alh.Column(alh.String(length=60), unique=True)
    id_en_word = alh.Column(alh.Integer, ForeignKey('english_word.id_english_word', ondelete='CASCADE'))
    def __str__(self):
        return f'{self.word}'

class English_word(Base):
    __tablename__ = "english_word"

    id_english_word = alh.Column(alh.Integer, primary_key=True)
    word = alh.Column(alh.String(length=60), unique=True)
    # id_russ_word = alh.Column(alh.Integer, ForeignKey('russian_word.id_russian_word', ondelete='CASCADE'))
    id_user_w = alh.Column(alh.Integer, ForeignKey('program_user.id_p_user', ondelete='CASCADE'))
    def __str__(self):
        return f'{self.word}'





def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
