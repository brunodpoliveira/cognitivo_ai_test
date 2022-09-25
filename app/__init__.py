from flask import Flask, Blueprint
from flask_restplus import Api
from werkzeug.middleware.proxy_fix import ProxyFix
from app.main.store.store_controller import api as home_ns
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
blueprint = Blueprint('api', __name__)
app.register_blueprint(blueprint)
db_path = os.path.join(os.path.dirname(__file__), '../static/local_db.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = "random string"
app.engine = create_engine(db_uri, echo=True)
eng_exp = app.engine
db = SQLAlchemy(app)

authorizations = {
    'bearer': {
        'name': "Authorization",
        'in': "header",
        'type': "apiKey",
        'description': "Insert your JWT Token here!"
    }
}
api = Api(app, title='Cognitivo.Ai - Teste de backend', version='0.1', description='Teste de API para Cognitivo.Ai',
          prefix='/api', authorizations=authorizations)

api.add_namespace(home_ns, path='/store')
