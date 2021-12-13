# Create your tests here.

import os
import unittest
from unittest import TestCase
from datetime import date
from app import app, db, bcrypt
from app.models import Game, User, Play


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_game():
    g1 = Game(name='Seahawks')
    model1 = Game(
        game=g1,
        desc='Seahawks beat the 49ers',
        yards=300,
    )
    db.session.add(model1)

    g2 = Game(name='Seahawks')
    model2 = Game(
        game=g2,
        desc='Seahawks beat the 49ers',
        yards=300,
    )
    db.session.add(model1)
    db.session.add(model2)
    db.session.commit()

def create_play():
    m1 = Play(name='Rams')
    db.session.add(m1)
    db.session.commit()
    
    

def create_user():
    password_hash = bcrypt.generate_password_hash('pass').decode('utf-8')
    user = User(username='iggi', password=password_hash)
    db.session.add(user)
    db.session.commit()

class MainTests(unittest.TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_create_play(self):
        create_user()
        create_play()

        login(self.app, 'iggi', 'pass')

        play_post = {
            "game": "Seahawks",
            "desc": "Seahawks played the Broncos",
            "yards": 300
        }
        self.app.post('/create_play', data=play_post)

        play_created = Play.query.filter_by(model='Seahawks').one()

        self.assertIsNotNone(play_created)
        self.assertEqual(play_created.game.name, 'Jags')

    def test_create_game(self):
        """Test to see if we can create a game"""
        create_user()
        create_game()

        login(self.app, 'iggi', 'pass')

        game_post = {
            "name": 3
        }
        self.app.post('/create_game', data=game_post)

        game_created = Game.query.filter_by(name='49ers').one()
        self.assertIsNotNone(game_created)
        self.assertEqual(game_created.name, '49ers')

    def test_create_play_logged_out(self):
        """see if the user is not able to create a play if they are logged out"""
        create_play()
        create_user()
        response = self.app.get('/create_play')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_play', response.location)