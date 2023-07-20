from mongoengine import Document
from mongoengine.fields import DateTimeField, ListField, StringField, ReferenceField
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from connect import engine


class Author(Document):
    fullname = StringField()
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


Base = declarative_base()

quote_tag_association = Table('quote_tag_association', Base.metadata,
                              Column('quote_id', Integer, ForeignKey('quotes.id')),
                              Column('tag_id', Integer, ForeignKey('tags.id'))
                              )


class PQuote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    quote = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('PAuthor', back_populates='quotes')

    tags = relationship('PTag', secondary=quote_tag_association, back_populates='quotes')


class PTag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    quotes = relationship('PQuote', secondary=quote_tag_association, back_populates='tags')


class PAuthor(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    born_date = Column(String)
    born_location = Column(String)
    description = Column(String)
    quotes = relationship('PQuote', back_populates='author')


Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
