import jwt
from datetime import datetime, timedelta
from flask import jsonify, request

from backend.models import User, db
from . import api


@api.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.authenticate(**data)
    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401
    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=30)
        # TODO: This is a hack until the pythonanywhere server issue resolved
    }, b'\xcf\xdcp\xe0\xbd;\xd4%#\x16\xdf_doc_prop\x05\xfc\xcd_\x0f'
    )
    return jsonify({'token': token.decode('UTF-8')})
