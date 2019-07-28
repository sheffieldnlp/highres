import http
import json
from flask import jsonify, request

from . import api
from backend.models import Document, AnnotationResult


@api.route('/document/<doc_id>', methods=['GET'])
def api_document_get(doc_id):
    if request.method == 'GET':
        doc_json = json.dumps(Document.get_dict(doc_id))
        if doc_json:
            return jsonify(doc_json), http.HTTPStatus.Ok


@api.route('/document/get_one', methods=['GET'])
def api_document_get_one():
    documents = Document.query.all()
    for document in documents:
        for doc_status in document.doc_statuses:
            n_results = len(AnnotationResult.query.filter_by(id=doc_status.id).all())
            if doc_status.total_exp_results == n_results:
                continue
            else:
                return jsonify(document.to_dict())
    return '', http.HTTPStatus.NO_CONTENT
