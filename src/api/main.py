from flask import request
from flask_restx import Resource, Api, Namespace

Main = Namespace('Main')

@app.route('/')
def main():
    return render_template('index.html')