# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Game, User, Play

class PlayForm(FlaskForm):
    
    desc = StringField('Desc', validators=[DataRequired(), Length(min=1, max=280)])
    yards = StringField('Yards', validators=[DataRequired(), Length(min=1, max=280)])
    submit = SubmitField('Submit')

class GameForm(FlaskForm):
    """Form to enter Game that was played."""
    name = StringField('Game',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')