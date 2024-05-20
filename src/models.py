import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
#from enum import Enum

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    firstname = Column(String(30))
    lastname = Column(String(30))
    email = Column(String(50), unique=True)
    posts = relationship("Post", back_populates = "user")
    comments = relationship("Comment", back_populates = "author")
    followers = relationship("Follower", foreign_keys = "Follower.user_to_id")
    following = relationship("Follower", foreign_keys = "Follower.user_from_id")
        
class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'))
    user_to_id = Column(Integer, ForeignKey('user.id'))


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates = "post")
    comments = relationship("Comment", back_populates = "post")
    media = relationship("Media", back_populates = "post")




class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('comment','media', name = "media_type"))
    url = Column(String(50))
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", back_populates = "media")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(50))
    author_id = Column(Integer, ForeignKey('user.id'))
    author_id_relationship = relationship(User)
    post_id = Column(Integer, ForeignKey('post.id'))
    author = relationship("User", back_populates = "comments")
    post = relationship("Post", back_populates = "comments")


    

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
