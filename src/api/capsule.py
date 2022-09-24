from flask import Blueprint, session, request, jsonify, redirect, url_for, render_template
import datetime
import models

Capsule = Blueprint('Capsule', __name__)

def get_year():
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    return year

@Capsule.route('/capsule', methods=['GET'])
def capsule():
    pass #get
    user_id = session.get('userid')
    if user_id is not None:
        year = get_year()
        post = models.Capsule.query.filter_by(user_id=user_id, post_at=year).first()
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
    year = request.form.get('year')
    content = request.form.get('content')
    return redirect(url_for('capsule')) # create, index로 redirect

@Capsule.route('/capsule/tmp/save', methods=['POST'])
def temp_save():
    year = request.form.get('year')
    content = request.form.get('content')
    return jsonify({'status':'success'}) # create, ajax 사용

@Capsule.route('/capsule/<int:id>', methods=['PUT'])
def update():
    pass # update