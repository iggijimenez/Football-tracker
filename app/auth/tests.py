# Create your tests here.

import os
import unittest
from unittest import TestCase

from datetime import date
 
from app import app, db, bcrypt
#change ------------------------
from app.models import Game, Manufacturer, Play, User, Vehicle

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
    # Creates a user with username 'igg' and password of 'password'
    password_hash = bcrypt.generate_password_hash('pass').decode('utf-8')
    user = User(username='iggi', password=password_hash)
    db.session.add(user)
    db.session.commit()

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_login_incorrect_password(self):
        """test to see if the user can log in with an incorrect password"""
        create_user()
        sample_data = {
            "username": "iggi",
            "password": "nopass",
        }
    
        
        response = self.app.post("/login", data=sample_data)
     
        response_msg = response.get_data(as_text=True)
        self.assertIn("Log In", response_msg)
      
        self.assertIn(
            "Password doesnt match. Please try again.", response_msg
        )
        self.assertNotIn("Log Out", response_msg)

    def test_logout(self):
        """test logout"""
  
        create_user()
        sample_data = {
            "username":"iggi1",
            "password":"helloWorld"
        }
        
        self.app.post("/login", data=sample_data)

        response = self.app.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_msg = response.get_data(as_text=True)
        
        self.assertIn("Log In", response_msg)
        self.assertNotIn("Log Out", response_msg)

    def test_login_nonexistent_user(self):
        """test a nonexistent user, make sure it fails"""
       
        sample_data = {
            "username": "nonexistent_user",
            "password": "hacked",
        }
        response = self.app.post("/login", data=sample_data)

        response_msg = response.get_data(as_text=True)
        self.assertIn("Log In", response_msg)
        self.assertIn(
            "No user with that username. Please try again.", response_msg
        )
        self.assertNotIn("Log Out", response_msg)