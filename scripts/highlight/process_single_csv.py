import os
import pandas as pd
import json

from backend.models import AnnotationResult
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    app = create_app()
    db = SQLAlchemy(app)
    file_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/mturk/working/Batch_3463189_batch_results.csv'
    df = pd.read_csv(file_path, delimiter=',')

    for i in df.index:
        code = df['Answer.surveycode'][i]
        result = db.session.query(AnnotationResult).filter(
            AnnotationResult.mturk_code.like('%' + code + '%')).first()
        if result:
            result_json = json.loads(result.result_json)
            validity = result.validity
            if validity:
               feedback = ''
            else:
                feedback = 'You did not answer the True/False question correctly. Sorry for that.'
            if len(result_json['highlights']) == 0:
                validity = False
                feedback = 'You did not do the highlighting.'
            if validity:
                df['Approve'][i] = 'x'
            else:
                df['Reject'][i] = feedback
    df.to_csv(file_path, header=df.columns.values)
