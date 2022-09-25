from flask import Flask, Blueprint
from flask_restplus import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from app.main.store.store_controller import api as home_ns

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
blueprint = Blueprint('api', __name__)
app.register_blueprint(blueprint)

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
