import pandas as pd
import json

from backend.models import EvaluationResult
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    app = create_app()
    db = SQLAlchemy(app)

    results = db.session.query(EvaluationResult).all()
    for result in results:
        validity = result.validity
        if result.precision == 50.0 and result.recall == 50.0:
            validity = False
        if not validity:
            db.session.delete(result)
            db.session.commit()
