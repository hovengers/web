from flask import Blueprint, render_template, session, redirect, url_for
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

        # 랜덤 메시지 30개
        sql = "SELECT message FROM "+ config.db['database'] +".kkt_message_counts ORDER BY RAND() LIMIT 30"
        curs.execute(sql)
        data = curs.fetchall()
        msg_random = []
        for i in range(0, 30, 1):
            msg_random.append(data[i][0])

        # 가장 많이 말한 메시지
        sql = "SELECT message, MAX(counts) FROM "+ config.db['database'] +".kkt_message_counts"
        curs.execute(sql)
        data = curs.fetchall()
        msg_most = data[0][0]

        # 가장 많고 적은 대화 날짜(이거 한 상위 5개 하위 5개로 못하려나)
        sql = "SELECT * FROM "+ config.db['database'] +".kkt_date_counts ORDER BY counts DESC"
        curs.execute(sql)
        data = curs.fetchall()
        date_most = data[0][0]
        date_most_list = []
        for i in range(0, 5, 1):
            date_most_list.append(data[i][0])

        sql = "SELECT * FROM "+ config.db['database'] +".kkt_date_counts ORDER BY counts"
        curs.execute(sql)
        data = curs.fetchall()
        date_least = data[0][0]
        date_least_list = []
        for i in range(0, 5, 1):
            date_least_list.append(data[i][0])

        # 가장 많고 적은 대화 시간(얘도...)
        sql = "SELECT * FROM "+ config.db['database'] +".kkt_time_counts ORDER BY counts DESC"
        curs.execute(sql)
        data = curs.fetchall()
        time_most = data[0][0]
        time_most_list = []
        for i in range(0, 5, 1):
            time_most_list.append(data[i][0])

        sql = "SELECT * FROM "+ config.db['database'] +".kkt_time_counts ORDER BY counts ASC"
        curs.execute(sql)
        data = curs.fetchall()
        time_least = data[0][0]
        time_least_list = []
        for i in range(0, 5, 1):
            time_least_list.append(data[i][0])

        # 대화 시간 그래프 있으면 좋을텐데 plt 그래프 저장할말

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
        sql = "SELECT * FROM "+ config.db['database'] +".kkt_user_counts ORDER BY counts DESC;"
        curs.execute(sql)
        data = curs.fetchall()
        user_list = []
        for i in range(0, len(data) - 1, 1):
            user_list.append([data[i][0], data[i][1]])

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
        for i in range(0, len(data) - 1, 1):
            day_talk_list.append([data[i][0], data[i][1]])

        con.close()

        res = {
            'username':session.get('username'),
            'msg_total':msg_total,
            'msg_random':msg_random,
            'msg_most':msg_most,

            'date_most':date_most,
            'date_most_list':date_most_list,
            'date_least':date_least,
            'date_least_list':date_least_list,

            'time_most':time_most,
            'time_most_list':time_most_list,
            'time_least':time_least,
            'time_least_list':time_least_list,

            'user_most':user_most,
            'user_least':user_least,
            'user_list':user_list,

            'num_freq':num_freq,
            'talk_rank':talk_rank,
            'talk_avg':talk_avg,
            'day_talk_rank':day_talk_rank,
            'day_talk_list':day_talk_list
        }
        return render_template('kakaotalk/index.html', data=res)
    else:
        return redirect(url_for('signin'))