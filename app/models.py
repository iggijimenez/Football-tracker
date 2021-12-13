from app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(280), nullable=False)
    plays = db.relationship('Play', back_populates='game')

class Play(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(280), nullable=False)
    yards = db.Column(db.Integer, nullable=False)
    
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    Game = db.relationship('Game', back_populates='plays')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)