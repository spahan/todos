from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from views import *

login_manager.user_loader(load_user)


if app.config['DEBUG']:
    import logging
    import http.client

    http.client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


if __name__ == '__main__':
    app.run('0.0.0.0', debug=app.config['DEBUG'])