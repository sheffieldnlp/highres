import pytest
from backend.app import create_app
from backend.models import db
from flask_sqlalchemy import SQLAlchemy
from scripts.insert_dataset import init_database


flask_app = None


def get_app():
    global flask_app
    if not flask_app:
        flask_app = create_app('test.cfg.py')
    return flask_app


@pytest.fixture(scope='module')
def test_client():
    app = get_app()
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture(scope='module')
def init_db():
    app = get_app()
    db.init_app(app)
    db.create_all()
    db.session.commit()
    init_database(db)
    yield db
    db.drop_all()
