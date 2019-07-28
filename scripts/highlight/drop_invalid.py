import pandas as pd
import json

from backend.models import AnnotationResult
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    app = create_app()
    db = SQLAlchemy(app)

    results = db.session.query(AnnotationResult).all()
    for result in results:
        if result.result_json:
            result_json = json.loads(result.result_json)
            validity = result.validity
            if len(result_json['highlights']) == 0:
                validity = False
            if not validity:
                db.session.delete(result)
                db.session.commit()
        else:
            db.session.delete(result)
            db.session.commit()
