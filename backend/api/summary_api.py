import http
from flask import jsonify

from . import api
from backend.models import SummariesPair, SummaryGroup, Summary


@api.route('/summ_group', methods=['GET'])
def api_summ_group_get_names():
    summ_groups = SummaryGroup.query.all()
    if not summ_groups:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        result = dict()
        result['names'] = []
        for summ_group in summ_groups:
            result['names'].append(summ_group.name)
        return jsonify(result)
