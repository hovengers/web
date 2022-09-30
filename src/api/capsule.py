from flask import Blueprint, session, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
import models

db = SQLAlchemy()
Capsule = Blueprint('Capsule', __name__)

def get_year():
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    return year

def get_date():
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    # res = date.strftime("%Y-%M-%D")
    return date

def conv_postdate(year):
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    res = date.strftime("-%M-%D")
    return year+res

@Capsule.route('/capsule', methods=['GET'])
def capsule():
    pass #get
    user_id = session.get('userid')
    if user_id is not None:
        date = get_date()
        post = models.Capsule.query.filter_by(user_id=user_id, post_at=date).first()
        print(post)
        if post is not None:
            res = {
                "status":"success", 
                "post":post
                }
            return render_template('capsule/index.html', data=res)          
        else:
            res = {
                "status":"success", 
                "message":"올해 얻은 캡슐이 없어요!"
                }
            return render_template('capsule/index.html', data=res)
    else:
        return redirect(url_for('signin'))


@Capsule.route('/capsule/new', methods=['GET'])
def new():
    cur_year = get_year()
    year = [int(cur_year)+1, int(cur_year)+3, int(cur_year)+5]
    return render_template('capsule/new.html', years=year) # new, 글쓰기 페이지
    
@Capsule.route('/capsule/save', methods=['POST'])
def save():
    cur_date = get_date()
    post_date = conv_postdate(request.form.get('year'))
    content = request.form.get('content')
    new_cap = models.Capsule(
        user_id=session.get('userid'),
        content=content,
        created_at=cur_date,
        post_at=post_date,
        status=True
        )
    db.session.add(new_cap)
    db.session.commit()
    return redirect(url_for('capsule')) # create, index로 redirect

@Capsule.route('/capsule/tmp/save', methods=['POST'])
def temp_save():
    cur_date = get_date()
    post_date = conv_postdate(request.form.get('year'))
    content = request.form.get('content')
    new_cap = models.Capsule(
        user_id=session.get('userid'),
        content=content,
        created_at=cur_date,
        post_at=post_date,
        status=False
        )
    db.session.add(new_cap)
    db.session.commit()
    return jsonify({'status':'success'}) # create, ajax 사용

@Capsule.route('/capsule/update/<int:id>', methods=['GET', 'PUT'])
def update():
    if request.method == 'PUT':
        cur_date = get_date()
        post_date = conv_postdate(request.form.get('year'))
        content = request.form.get('content')
        # update
    else:
        return render_template('capsule/update.html', postid=id)