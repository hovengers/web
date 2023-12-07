from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_cors import cross_origin
import pymysql
import config

Kakaotalk = Blueprint('Kakaotalk', __name__)

@Kakaotalk.route('/kakaotalk', methods=['GET'])
def kakaotalk():
    if session.get('userid') is not None:
        con = pymysql.connect(host=config.db['host'], user=config.db['user'], password=config.db['password'], db=config.db['database'], charset='utf8')
        curs = con.cursor()

        # 총 메시지 개수
        sql = "SELECT FORMAT(total, 0) FROM "+ config.db['database'] +".kkt_msg_total"
        curs.execute(sql)
        data = curs.fetchall()
        msg_total = data[0][0]


        # 연도별 메시지 개수
        sql = "SELECT year, FORMAT(counts, 0) FROM "+ config.db['database'] +".kkt_year_counts"
        curs.execute(sql)
        data = curs.fetchall()
        year_list = []
        start_year = data[0][0]
        end_year = data[len(data) - 1][0]
        for d in data:
            year_list.append(d)


        # 월별 대화량
        sql = "SELECT month, FORMAT(counts, 0) FROM "+ config.db['database'] +".kkt_month_counts ORDER BY counts DESC"
        curs.execute(sql)
        data = curs.fetchall()
        month_most = data[0][0]
        month_least = data[len(data) - 1][0]
        month_list = []
        for month in data:
            month_list.append(month)


        # 가장 많고 적은 대화 날짜
        sql = "SELECT date, FORMAT(counts, 0) FROM "+ config.db['database'] +".kkt_date_counts ORDER BY counts DESC"
        curs.execute(sql)
        data = curs.fetchall()
        date_most = data[0][0]
        date_most_list = []
        for i in range(0, 5, 1):
            date_most_list.append(data[i])

        sql = "SELECT date, FORMAT(counts, 0) FROM "+ config.db['database'] +".kkt_date_counts ORDER BY counts"
        curs.execute(sql)
        data = curs.fetchall()
        date_least = data[0][0]
        date_least_list = []
        for i in range(0, 5, 1):
            date_least_list.append(data[i])


        # 가장 많고 적은 대화 시간(얘도...)
        sql = "SELECT time, FORMAT(counts, 0) FROM "+ config.db['database'] +".kkt_time_counts ORDER BY counts DESC"
        curs.execute(sql)
        data = curs.fetchall()
        time_most = data[0][0]
        time_least = data[len(data) - 1][0]
        time_list = []
        for time in data:
            time_list.append(time)
    

        # 랜덤 메시지 50개
        sql = "SELECT message FROM "+ config.db['database'] +".kkt_message_counts ORDER BY RAND() LIMIT 50"
        curs.execute(sql)
        data = curs.fetchall()
        msg_random = []
        for msg in data:
            msg_random.append(msg[0])


        # 가장 많이 말한 메시지 10개
        sql = "SELECT message, FORMAT(counts, 0) FROM "+ config.db['database'] +".kkt_message_counts ORDER BY counts DESC LIMIT 10"
        curs.execute(sql)
        data = curs.fetchall()
        msg_most = data[0][0]
        msg_most_count = data[0][1]
        msg_most_list = []
        for msg in data:
            msg_most_list.append(msg)


        # 가장 적게 말한 메시지 10개
        sql = "SELECT message, FORMAT(counts, 0) FROM "+ config.db['database'] +".kkt_message_counts ORDER BY counts LIMIT 10"
        curs.execute(sql)
        data = curs.fetchall()
        msg_least_list = []
        for msg in data:
            msg_least_list.append(msg)


        # 가장 많고 적게 말한 사람
        sql = "SELECT * FROM "+ config.db['database'] +".kkt_user_counts ORDER BY counts DESC"
        curs.execute(sql)
        data = curs.fetchall()
        user_most = data[0][0]
        user_least = data[len(data) - 1][0]


        # 톡방에서 몇 번 말했는지
        sql = "SELECT FORMAT(counts, 0) FROM "+ config.db['database'] +".kkt_user_counts WHERE user='"+session.get('userid')+"'"
        curs.execute(sql)
        data = curs.fetchall()
        num_freq = data[0][0]


        # 톡방 발언 순위
        sql = "SELECT user, rank() over (order by counts desc) FROM "+ config.db['database'] +".kkt_user_counts"
        curs.execute(sql)
        values = curs.fetchall()
        for value in values:
            if value[0] == session.get('userid'):
                talk_rank = value[1]


        # 전체 대화 랭킹도 보여주기
        sql = "SELECT user, FORMAT(counts, 0) FROM "+ config.db['database'] +".kkt_user_counts ORDER BY counts DESC;"
        curs.execute(sql)
        data = curs.fetchall()
        user_list = []
        for user in data:
            user_list.append(user)


        # 일평균 발언 횟수
        sql = "SELECT * FROM "+ config.db['database'] +".kkt_user_day_frequency WHERE user='"+session.get('userid')+"'"
        curs.execute(sql)
        data = curs.fetchall()
        talk_avg = data[0][1]


        # 일평균 발언 순위
        sql = "SELECT user, rank() over (order by frequency desc) FROM "+ config.db['database'] +".kkt_user_day_frequency"
        curs.execute(sql)
        values = curs.fetchall()
        for value in values:
            if value[0] == session.get('userid'):
                day_talk_rank = value[1]


        # 전체 일평균 발언 순위
        sql = "SELECT * FROM "+ config.db['database'] +".kkt_user_day_frequency ORDER BY frequency DESC;"
        curs.execute(sql)
        data = curs.fetchall()
        day_talk_list = []
        for day in data:
            day_talk_list.append(day)

        # 며칠 전이 마지막 톡인지
        sql = "SELECT * FROM "+ config.db['database'] +".kkt_user_day_before ORDER BY day DESC;"
        curs.execute(sql)
        data = curs.fetchall()
        user_day_before = []
        for day in data:
            user_day_before.append(day)

        con.close()

        res = {
            'username':session.get('username'),
            'msg_total':msg_total,
            
            'start_year':start_year,
            'end_year':end_year,
            'year_list':year_list,

            'month_most':month_most,
            'month_least':month_least,
            'month_list':month_list,

            'date_most':date_most,
            'date_most_list':date_most_list,
            'date_least':date_least,
            'date_least_list':date_least_list,

            'time_most':time_most,
            'time_least':time_least,
            'time_list':time_list,

            'msg_random':msg_random,
            'msg_most':msg_most,
            'msg_most_count':msg_most_count,
            'msg_most_list':msg_most_list,
            'msg_least_list':msg_least_list,

            'user_most':user_most,
            'user_least':user_least,
            'user_list':user_list,

            'num_freq':num_freq,
            'talk_rank':talk_rank,
            'talk_avg':talk_avg,
            'day_talk_rank':day_talk_rank,
            'day_talk_list':day_talk_list,
            'user_day_before':user_day_before
        }
        return render_template('kakaotalk/index.html', data=res)
    else:
        return redirect(url_for('Account.signin'))
    
@Kakaotalk.route('/kakaotalk/search', methods=['GET'])
def search():
    word = request.args.get('word')

    con = pymysql.connect(host=config.db['host'], user=config.db['user'], password=config.db['password'], db=config.db['database'], charset='utf8')
    curs = con.cursor()

    sql = "SELECT message FROM "+ config.db['database'] +".kkt_message_counts WHERE message LIKE '%"+ word +"%';"
    curs.execute(sql)
    data = curs.fetchall()
    msg = []
    for val in data:
        msg.append(val[0])

    con.close()

    return jsonify({'msg':msg})