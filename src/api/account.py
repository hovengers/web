from sqlite3 import DatabaseError
from flask import current_app, Blueprint, request, render_template, jsonify, session, redirect, url_for
import models
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()
Account = Blueprint('Account', __name__)

@Account.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        hashpw = bcrypt.hashpw(request.form.get('pw').encode("utf-8"), bcrypt.gensalt())
        print(bcrypt.checkpw(request.form.get('pw').encode("utf-8"), hashpw))
        new_user = models.User(id=request.form.get('id'), password=hashpw, name=request.form.get('name'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('Account.signin'))
    else:
        return render_template('account/signup.html')

@Account.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method =='POST':
        try:
            data = models.User.query.filter_by(id=request.form.get('id')).first()
            print(data.password, ", ", bcrypt.checkpw(request.form.get('pw').encode('utf-8'), data.password.encode('utf-8')))
            if data and bcrypt.checkpw(request.form.get('pw').encode('utf-8'), data.password.encode('utf-8')):
                session['userid'] = data.id
                session['username'] = data.name
                return redirect(url_for('Main.main'))
            else:
                return render_template('account/signin.html', status='로그인에 실패했습니다.')
        except:
            return render_template('account/signin.html', status='로그인에 실패했습니다.')
    else:
        return render_template('account/signin.html')

@Account.route('/signout')
def signout():
    session.pop('userid', None)
    session.pop('username', None)
    return redirect(url_for('Main.main'))