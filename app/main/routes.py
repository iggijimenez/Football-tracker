# Create your routes here.
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from ..models import Game, Play
from app.main.forms import PlayForm, GameForm


from app import app, db

main = Blueprint("main", __name__)



##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    all_play = Play.query.all()
    return render_template('homepage.html', all_plays=all_play)


@main.route('/create_play', methods=['GET', 'POST'])
@login_required
def new_play():
    form = PlayForm()

    if form.validate_on_submit():
        new_play = Play(
            game=form.game.data,
            desc=form.desc.data,
            yards=form.yards.data
        )

        db.session.add(new_play)
        db.session.commit()

        flash('Your Play was created!')
        return redirect(url_for('main.homepage'))
    return render_template('new_play.html', form=form)

@main.route('/create_game', methods=['GET', 'POST'])
@login_required
def create_game():
    form = GameForm()
    if form.validate_on_submit():
        new_game = Game(
            name=form.name.data,
        )
        db.session.add(new_game)
        db.session.commit()

        flash('New Game added successfully.')
        return redirect(url_for('.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('new_game.html', form=form)


@main.route('/play/<play_id>', methods=['GET', 'POST'])
def play_detail(play_id):
    play = Play.query.get(play_id)
    form = PlayForm(obj=play)
    
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        play.model = form.model.data
        play.desc = form.desc.data

        db.session.commit()

        flash('Play was updated successfully.')
        return redirect(url_for('main.play_detail', play_id=play_id))

    return render_template('play_detail.html', play=play, form=form)