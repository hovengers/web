from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
import kkt.config as config

from api.main import Main
from api.account import Account
from api.capsule import Capsule
from api.kakaotalk import Kakaotalk

app = Flask(__name__)

bcrypt = Bcrypt(app)
CORS(app, support_credentials=True)

# api = Api(
#             app,
#             version='0.1',
#             title="Hoee API Server",
#             description="Hoee blog API Server",
#             doc="/api-docs",
#             contact="hwgyuhyeon@gmail.com",
# )

# api
app.register_blueprint(Main)
app.register_blueprint(Account)
app.register_blueprint(Capsule)
app.register_blueprint(Kakaotalk)

# db 
app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)

# json
# return json value as utf8
app.config['JSON_AS_ASCII'] = False

# key
app.secret_key = config.SECRET_KEY
app.config['BCRYPT_LEVEL'] = 10


if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)