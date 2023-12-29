### Database connection ###
from sqlalchemy import create_engine
import config

db_connection = create_engine(config.DB_URI)
conn = db_connection.connect()



import pandas as pd

df = pd.read_csv('kkt/KakaoTalkChats.txt', delimiter = '\t')
for col in df.columns:
    origin = col
    num = col
num = int(num.split('(')[1].split(')')[0]) # 단톡방 인원수

### 컬럼을 사용자 정보와 메시지 내용으로 나누어서 각각 전처리 ###
df = df.drop(index=[0], axis=0) # 맨 위에 톡방 정보 지우기
df = df[origin].str.split(' : ', expand=True) # 작성자랑 내용 기준으로 나누고
df.rename(columns={0:'info', 1:'message'}, inplace=True) # 정보랑 메시지 나눔


### 메시지 빈도수 결과를 위한 한국어 대체 ###
df = df.replace({'message':'Emoticons'}, '(이모티콘)')
df = df.replace({'message':'<Photo Unread>'}, '(사진)')
df = df.replace({'message':'This message was deleted.'}, '삭제된 메시지입니다.')
df = df.replace({'message':'Live Talk started'}, '라이브톡 시작')
df = df.replace({'message':'Live Talk ended'}, '라이브톡 종료')

# 1. 메시지 점유율
### 메시지 개수 세서 테이블 kkt.message_counts 생성 ###
messagedf = df['message'].value_counts().rename_axis('message').reset_index(name='counts') # 메시지 개수 세기
messagedf.head(100).to_sql(name='kkt.message_counts', con=db_connection, if_exists='replace',index=False) # 테이블 생성

# 2. 카톡 시간 빈도
### df1: 사용자 정보만 떼온 df 전처리 ###
df1 = df.loc[:,'info']
df1 = df1.str.split(', ', expand=True) # 날짜, 연도, 시간, 사용자로 나눔
df1.rename(columns={0:'date', 1:'year', 2:'time',3:'user'}, inplace=True) # 정보랑 메시지 나눠서
df1 = df1.loc[:,'date':'user'] # 유의미한 정보 있는 4개 열만 살리고
df1.dropna(inplace=True) # 결측치 제거
df1.drop(df1[df1['user'] == 'This message was deleted.'].index, inplace=True) # 사용자에 메시지가 있는 결측치 제거


### datedf: 날짜별 메시지 수를 저장해둔 df => kkt_date_counts ### 
datedf = df1['date'].value_counts().rename_axis('date').reset_index(name='counts')
datedf.drop(datedf[datedf['counts'] <= 30].index, inplace=True)

from datetime import datetime
def df1_date_convert(datestr): # convert date to Korean
    day = datestr.split(' ')[1]
    month = datestr.split(' ')[0]
    try:
        datetime_object = datetime.strptime(month, "%B")
    except ValueError:
        return None
    month_num = datetime_object.month
    return str(month_num) + '월 ' + day + '일'

datedf['date'] = datedf['date'].apply(df1_date_convert)
datedf.to_sql(name='kkt_date_counts', con=db_connection, if_exists='replace',index=False)


### yeardf: 연도별 메시지 수를 저장해둔 df => kkt_year_counts ###
yeardf = df1['year'].value_counts(sort=False).rename_axis('year').reset_index(name='counts')
yeardf.drop(yeardf[yeardf['counts'] <= 50].index, inplace=True)
yeardf.to_sql(name='kkt_year_counts', con=db_connection, if_exists='replace',index=False)


### monthdf: 월별 메시지 수를 저장해둔 df => kkt_month_counts ###
monthdf = df1['date'].value_counts().rename_axis('month').reset_index(name='counts')
monthdf.drop(monthdf[monthdf['counts'] <= 30].index, inplace=True)

def df1_month_convert(datestr): # convert date to Korean
    month = datestr.split(' ')[0]
    try:
        datetime_object = datetime.strptime(month, "%B")
    except ValueError:
        return None
    month_num = datetime_object.month
    return str(month_num) + '월'

monthdf['month'] = monthdf['month'].apply(df1_month_convert)
monthdf.groupby('month').sum().reset_index().to_sql(name='kkt_month_counts', con=db_connection, if_exists='replace',index=False)

### timedf: 시간별 메시지 수를 저장해둔 df ###
def df1_time_convert(str): # 시간 포맷을 1:00 PM => 13으로 변환
    if str is None:
        return None
    if str[-2:] == 'AM':
        hour = int(str.split(':')[0])
        if hour == 12:
            hour = 0
        return hour
    elif str[-2:] == 'PM':
        hour = int(str.split(':')[0]) + 12
        if hour == 24:
            hour = 12
        return hour
    
df1['time'] = df1['time'].apply(df1_time_convert)

timedf = df1['time'].value_counts(sort=False).rename_axis('time').reset_index(name='counts')
timedf = timedf.astype('int64') # time이 object임.. 그래서 int로 변경
timedf = timedf.sort_values(by='time') # 사용자 길이별로 정렬
timedf.set_index('time', drop=True, inplace=True) # 시간을 인덱스로 변경!
timedf.to_sql(name='kkt_time_counts', con=db_connection, if_exists='replace',index=True)


# 3. 사용자 점유율
### userdf: 사용자별 메시지 개수를 저장해둔 df ###
userdf = df1['user'].value_counts().rename_axis('user').reset_index(name='counts') # 참가자명 df 생성
userdf = userdf.sort_values(by='user', key=lambda x: x.str.len()) # 사용자 길이별로 정렬
userdf.reset_index(drop=True, inplace=True) # 인덱스 재정렬(드랍용)
userdf = userdf.sort_values('counts', ascending=False)
userdf.reset_index(drop=True, inplace=True) # 인덱스 재정렬(드랍용)
userdf = userdf.take(userdf.index[0:num]) # 단톡방 참여자 수 제외하고 전부 드랍
userdf.to_sql(name='kkt_user_counts', con=db_connection, if_exists='replace',index=False)


# 4. 마지막 카톡 날짜
### df2: date, year를 datetime(2020-01-01)으로 포맷 변경한 df
df2 = df1.copy()

from datetime import datetime

def df2_year_val(yearstr):
    try:
        val = int(yearstr)
    except ValueError:
        return None
    return yearstr

def df2_date_convert(datestr):
    zero_string_month = ""
    zero_string_day = ""    
    
    if (len(datestr.split(' ')) > 1):
        day = datestr.split(' ')[1]
    else:
        day = '0'
    month = datestr.split(' ')[0]
    try:
        datetime_object = datetime.strptime(month, "%B")
    except ValueError:
        return None
    month_num = datetime_object.month
    
    if int(day) < 10:
        zero_string_day = '0'
    if month_num < 10:
        zero_string_month = '0'
    return zero_string_month + str(month_num) + '-' + zero_string_day + day

df2['year'] = df2['year'].apply(df2_year_val)
df2['date'] = df2['date'].apply(df2_date_convert)
df2.dropna(inplace=True)

def df2_datetime_gen(col1, col2):
    res = col1
    if not pd.isna(col2):
        res += '-' + str(col2)
    return res

df2['datetime'] = df2.apply(lambda x: df2_datetime_gen(x['year'], x['date']), axis=1)

# 전체 메시지 개수 저장(결측치 최대 제거 버전이 df2)
raw_data = {'total': [len(df2)]}

msgtotal = pd.DataFrame(raw_data)
msgtotal.to_sql(name='kkt_msg_total', con=db_connection, if_exists='replace',index=False)

# 사용자가 마지막으로 온 날
users = userdf['user'].values
series = pd.Series([0], index=['init'])

for user in users:
    ser = pd.Series([0], index=[user])
    index = df2[df2['user'] == user].index[-1:][0] # 마지막 대화 인덱스
    date = df2.loc[index]['datetime']
    last = df2.iloc[-1]['datetime']
    
    last = datetime.strptime(last,'%Y-%m-%d')
    date = datetime.strptime(date,'%Y-%m-%d')
    diff = last - date
    diff = str(diff)
    diff = diff.split(',')[0]
    val = 0
    if diff[0] != '0':
        val = int(diff.split(' ')[0])
    ser[user] = val
    series = pd.concat([series, ser], join='outer')

series.drop('init', inplace=True)
df3 = series.to_frame().reset_index()
df3.rename(columns={'index':'user', 0:'day'}, inplace=True)
df3 = df3.sort_values('day', ascending=False)
df3.to_sql(name='kkt_user_day_before', con=db_connection, if_exists='replace',index=False)


# 5. 사용자별 일평균 메시지 수
import datetime

### 시작날짜, 마지막날짜, diff ###
series = pd.Series([0], index=['init'])
first = df2.iloc[0]['datetime']
last = df2.iloc[-1]['datetime']
diff = datetime.datetime.strptime(last,'%Y-%m-%d') - datetime.datetime.strptime(first,'%Y-%m-%d')

### 날짜들만 따로 저장 ###
date_data = [['start', first], ['end', last], ['diff', diff]]
df_date = pd.DataFrame(date_data, columns=['Name','Value'])
df_date.to_sql(name='kkt_date', con=db_connection, if_exists='replace',index=False)

i = 0
for user in users:
    ser = pd.Series([0], index=[user])
    ser[user] = round(userdf.iloc[i][1] / diff.days, 2)
    i += 1
    series = pd.concat([series, ser], join='outer')
    
series.drop('init', inplace=True)
df4 = series.to_frame().reset_index()
df4.rename(columns={'index':'user', 0:'frequency'}, inplace=True)
df4.to_sql(name='kkt_user_day_frequency', con=db_connection, if_exists='replace',index=False)

conn.close()
db_connection.dispose()