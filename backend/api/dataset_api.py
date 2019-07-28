import http
from flask import jsonify

from . import api
from backend.models import Dataset


@api.route('/dataset/<dataset_name>', methods=['GET'])
def api_dataset_get_single(dataset_name):
    dataset = Dataset.query.filter_by(name=dataset_name).first()
    if not dataset:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return jsonify(dataset.to_dict())


@api.route('/dataset', methods=['GET'])
def api_dataset_get_names():
    datasets = Dataset.query.all()
    if not datasets:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        result = dict()
        result['names'] = []
        for dataset in datasets:
            result['names'].append(dataset.name)
        return jsonify(result)
