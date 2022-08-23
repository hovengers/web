from importlib.resources import Resource
from flask_restx import Resource, Namespace

Main = Namespace('Main')

@Main.route('')
class MainAPI(Resource):
    def main(self):
        return {"hello":"world!"}