import sqlalchemy as alh
from sqlalchemy import PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship, declared_attr, declarative_base


Base = declarative_base()

class Program_user(Base):
    __tablename__ = "program_user"

    id_p_user = alh.Column(alh.BIGINT, primary_key=True)
    name = alh.Column(alh.String(length=60))

    def __str__(self):
        return f'{self.name}'

class Word(Base):
    __tablename__ = "word"

    id_word = alh.Column(alh.Integer, primary_key=True)
    russian_word = alh.Column(alh.String(length=60), unique=True)
    english_word = alh.Column(alh.String(length=60), unique=True)
    id_user = alh.Column(alh.BIGINT, ForeignKey('program_user.id_p_user', ondelete='CASCADE'))
    def __str__(self):
        return f'{self.russian_word} {self.english_word}'

class Common_word(Base):
    __tablename__ = "common_word"

    id_common_word = alh.Column(alh.Integer, primary_key=True)
    russian_word = alh.Column(alh.String(length=60), unique=True)
    english_word = alh.Column(alh.String(length=60), unique=True)

    def __str__(self):
        return f'{self.russian_word} {self.english_word}'





def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
