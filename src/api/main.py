from flask import Blueprint, render_template, session

Main = Blueprint('Main', __name__)

@Main.route('/', methods=['GET', 'POST'])
def main():
    if session.get('username'):
        return render_template('index.html', name=session.get('username'))
    else:
        return render_template('index.html')