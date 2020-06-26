from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/match')
def match():
    return render_template('match.html')


@main.route('/recognition')
def recognition():
    return render_template('recognition.html')