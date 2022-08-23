from flask import Flask
from flask_restx import Api
from api.main import Main
from api.capsule import Capsule

app = Flask(__name__)
api = Api(
            app,
            version='0.1',
            title="Hoee API Server",
            description="Hoee blog API Server",
            terms_url="/",
            contact="hwgyuhyeon@gmail.com",
)

    
api.add_namespace(Main, '')
api.add_namespace(Capsule, '/capsule')


if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)