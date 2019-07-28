import os
import csv
import json

from backend.models import AnnotationResult
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    app = create_app()
    db = SQLAlchemy(app)
    csv_folder = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/mturk/csv'
    to_write = []
    no = 1
    for file in os.listdir(csv_folder):
        with open(os.path.join(csv_folder, file), newline='') as infile:
            reader = csv.DictReader(infile, delimiter=',')
            for row in reader:
                code = row['Answer.surveycode']
                result = db.session.query(AnnotationResult).filter(
                    AnnotationResult.mturk_code.like('%'+code+'%')).first()
                if result:
                    result_json = json.loads(result.result_json)
                    validity = result.validity
                    if len(result_json['highlights']) == 0:
                        validity = False
                    to_write.append({'No': no, 'Validity': validity,
                                     'Code': code, 'Len': len(result_json['highlights']),
                                     'File': file})
                    no += 1
    csv_write_folder = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/mturk'
    with open(os.path.join(csv_write_folder, 'result.csv'), 'w', newline='') as infile:
        writer = csv.DictWriter(infile, fieldnames=['No', 'Code', 'Len', 'Validity', 'File'])
        writer.writerows(to_write)
