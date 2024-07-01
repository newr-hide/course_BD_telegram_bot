import sqlalchemy as alh
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class English_word(Base):
    __tablename__ = "english_word"

    id_english_word = alh.Column(alh.Integer, primary_key=True)
    word = alh.Column(alh.String(length=60), unique=True)

    def __str__(self):
        return f'{self.word}'

class Russian_word(Base):
    __tablename__ = "russian_word"

    id_russian_word = alh.Column(alh.Integer, primary_key=True)
    word = alh.Column(alh.String(length=60), unique=True)

    def __str__(self):
        return f'{self.id_russian_word}: {self.word}'

class Bridge_russ_en_word:
    id_english_word = alh.Column(alh.Integer, alh.ForeignKey("english_word"),primary_key=True, nullable=False)
    id_russian_word = alh.Column(alh.Integer, alh.ForeignKey("russian_word"),primary_key=True, nullable=False)


    def __str__(self):
        return f'{self.id_english_word}: {self.id_russian_word}'
