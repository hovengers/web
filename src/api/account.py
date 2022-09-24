from flask import current_app, Blueprint, request, render_template, jsonify, session, redirect, url_for
import models
from flask_sqlalchemy import SQLAlchemy
import pymysql, config
import bcrypt

db = SQLAlchemy()
Account = Blueprint('Account', __name__)

@Account.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        hashpw = bcrypt.hashpw(request.form.get('pw').encode("utf-8"), bcrypt.gensalt())
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

@Account.route('/edit/password', methods=['GET', 'POST'])
def editpw():
    if request.method == 'POST':
        try:
            data = models.User.query.filter_by(id=session.get('userid')).first()
            if data and bcrypt.checkpw(request.form.get('c_pw').encode('utf-8'), data.password.encode('utf-8')):
                con = pymysql.connect(host=config.db['host'], user=config.db['user'], password=config.db['password'], db=config.db['database'], charset='utf8')
                curs = con.cursor()
                hashpw = bcrypt.hashpw(request.form.get('n_pw').encode('utf-8'), bcrypt.gensalt())
                print(type(hashpw))
                sql = "UPDATE "+ config.db['database'] +".user SET password=%s WHERE id=%s"
                curs.execute(sql, (hashpw, session.get('userid')))
                con.commit()
                con.close()
                return redirect(url_for('Main.main'))
            else:
                return render_template('account/editpw.html', status='비밀번호가 일치하지 않습니다.')
        except:
            return render_template('account/editpw.html', status='비밀번호가 일치하지 않습니다.')
    else:
        return render_template('account/editpw.html')

@Account.route('/edit/name', methods=['GET', 'POST'])
def editname():
    if request.method == 'POST':
        try:
            con = pymysql.connect(host=config.db['host'], user=config.db['user'], password=config.db['password'], db=config.db['database'], charset='utf8')
            curs = con.cursor()
            sql = "UPDATE "+config.db['database']+".user SET name=%s WHERE id=%s"
            curs.execute(sql, (request.form.get('n_name'), session.get('userid')))
            con.commit()
            con.close()
            session['username'] = request.form.get('n_name')
            return redirect(url_for('Main.main'))
        except:
            return render_template('account/editname.html', status='사용자 정보를 불러오는 데 실패했습니다. 관리자에게 문의해주세요.')
    else:
        return render_template('account/editname.html')