from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for
from models import user_model as db_user
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Account = Blueprint('Account', __name__)

@Account.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        new_user = db_user.User(id=request.form.get('id'), password=request.form.get('pw'), name=request.form.get('name'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signin'))
    else:
        return render_template('account/signup.html')
# 비밀번호 암호화때문에 회원가입 페이지를 만들어두지만
# 별도 회원가입 없이 이 페이지로 친구들 계정 미리 생성해주기
# 아이디는 실명, 초기 비밀번호는...

@Account.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method =='POST':
        id = request.form.get('id')
        pw = request.form.get('pw')
        try:
            data = db_user.User.query.filter_by(id=id, password=pw).first()
            if data:
                print(data.name)
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
    session.pop('username', None)
    return redirect(url_for('Main.main'))