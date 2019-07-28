import os
import jwt
from functools import wraps
from backend.models import db, User
from backend.api import api
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, make_response, request


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
    ))


def create_app(test_config=None):
    # Load .env file (create one if it doesn't exist)
    load_dotenv(os.path.join('../', '.env'))

    # create and configure the app
    app = CustomFlask(__name__, instance_relative_config=True,
                      static_folder='../../instance/dist/static',
                      template_folder='../../instance/dist')
    if test_config:
        app.config.from_pyfile(os.path.join(os.path.dirname(__file__), test_config))
    else:
        db_path = os.path.join(os.path.dirname(__file__), 'app.db')
        db_uri = 'sqlite:///{}'.format(db_path)
        app.config.from_mapping(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=db_uri,
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
        )
    app.register_blueprint(api)
    db.init_app(app)

    def token_required(f):
        @wraps(f)
        def _verify(*args, **kwargs):
            auth_headers = request.headers.get('Authorization', '').split()
            invalid_msg = {
                'message': 'Invalid token. Registration and / or authentication required',
                'authenticated': False
            }
            expired_msg = {
                'message': 'Expired token. Re-authentication required.',
                'authenticated': False
            }
            if len(auth_headers) != 2:
                return jsonify(invalid_msg), 401

            try:
                token = auth_headers[1]
                data = jwt.decode(token, app.config['SECRET_KEY'])
                user = User.query.filter_by(email=data['sub']).first()
                if not user:
                    raise RuntimeError('User not found')
                return f(user, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify(expired_msg), 401
            except (jwt.InvalidTokenError, Exception) as e:
                print(e)
                return jsonify(invalid_msg), 401

        return _verify

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/app.js')
    def send_app_js():
        headers = {"Content-Disposition": "attachment; filename=%s" % 'app.js'}
        path = os.path.join(app.instance_path, 'dist', 'app.js')
        with open(path, 'r') as f:
            body = f.read()
        return make_response((body, headers))

    return app
