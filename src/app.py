from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
import dbconfig

from api.main import Main
from api.capsule import Capsule

app = Flask(__name__)
api = Api(
            app,
            version='0.1',
            title="Hoee API Server",
            description="Hoee blog API Server",
            terms_url="/api",
            contact="hwgyuhyeon@gmail.com",
)

# api
api.register_blueprint(Main)
api.register_blueprint(Capsule)

# db 
app.config["SQLALCHEMY_DATABASE_URI"] = dbconfig.DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)

if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)