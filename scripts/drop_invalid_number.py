import pandas as pd
import json

from backend.models import AnnotationResult, DocStatus
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    app = create_app()
    db = SQLAlchemy(app)
    max = 10
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
    doc_statuses = db.session.query(DocStatus).all()
    for doc_status in doc_statuses:
        if len(doc_status.results) > max:
            prune = len(doc_status.results) - max
            i = 0
            for result in doc_status.results:
                db.session.delete(result)
                db.session.commit()
                i += 1
                if i >= prune:
                    break
