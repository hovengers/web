# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Capsule(db.Model):
    __tablename__ = 'capsule'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(45), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    post_at = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, nullable=False)



t_kkt_date_counts = db.Table(
    'kkt_date_counts',
    db.Column('date', db.Text),
    db.Column('counts', db.BigInteger)
)



t_kkt_message_counts = db.Table(
    'kkt_message_counts',
    db.Column('message', db.Text),
    db.Column('counts', db.BigInteger)
)



t_kkt_msg_total = db.Table(
    'kkt_msg_total',
    db.Column('total', db.BigInteger)
)



t_kkt_time_counts = db.Table(
    'kkt_time_counts',
    db.Column('time', db.BigInteger, index=True),
    db.Column('counts', db.BigInteger)
)



t_kkt_user_counts = db.Table(
    'kkt_user_counts',
    db.Column('user', db.Text),
    db.Column('counts', db.BigInteger)
)



t_kkt_user_day_before = db.Table(
    'kkt_user_day_before',
    db.Column('user', db.Text),
    db.Column('day', db.BigInteger)
)



t_kkt_user_day_frequency = db.Table(
    'kkt_user_day_frequency',
    db.Column('user', db.Text),
    db.Column('frequency', db.Float(asdecimal=True))
)



t_kkt_year_counts = db.Table(
    'kkt_year_counts',
    db.Column('year', db.Text),
    db.Column('counts', db.BigInteger)
)



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(70), nullable=False)
    name = db.Column(db.String(30), nullable=False)
