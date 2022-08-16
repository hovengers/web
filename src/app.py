from flask import flask
from flask_restx import Resource, Api
from api.main import main

app = Flask(__name__)
api = Api(app)

    
api.add_namespace(Main, '/')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)