import json
import http
import urllib.parse
import random
import string
from datetime import datetime, timedelta

from flask import jsonify, request

from . import api
from backend.models import \
    Document, AnnotationProject, AnnotationResult, \
    Dataset, DocStatus, ProjectType, EvaluationResult, \
    EvaluationProject, Summary, ProjectCategory, SummaryGroup


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


@api.route('/result/<project_type>/<status_id>', methods=['GET'])
def api_get_result_id(project_type, status_id):
    if project_type.lower() == ProjectType.ANNOTATION.value.lower():
        result_id = AnnotationResult.create_empty_result(status_id)
    elif project_type.lower() == ProjectType.EVALUATION.value.lower():
        result_id = EvaluationResult.create_empty_result(status_id)
    return jsonify(dict(result_id=result_id))


@api.route('/project/<project_type>/<project_category>/<project_id>/single_doc', methods=['GET'])
def api_project_single_doc(project_type, project_category, project_id):
    random.seed(datetime.now())
    if project_type.lower() == ProjectType.ANNOTATION.value.lower():
        project = AnnotationProject.query.get(project_id)
        if not project:
            return '', http.HTTPStatus.NOT_FOUND
        else:
            # Clean open project, very dirty
            for doc_status in project.doc_statuses:
                results = AnnotationResult.query.filter_by(status_id=doc_status.id, is_filled=False).all()
                for result in results:
                    if result.opened_at:
                        delta = datetime.utcnow() - result.opened_at
                        if delta >= timedelta(minutes=15):
                            AnnotationResult.del_result(result)
            # Retrieve result
            random_doc_statuses = list(project.doc_statuses)
            random.shuffle(random_doc_statuses)
            min_result = 999
            n_results_list = []
            for doc_status in random_doc_statuses:
                n_results = AnnotationResult.query.filter_by(status_id=doc_status.id).count()
                if n_results < min_result:
                    min_result = n_results
                n_results_list.append(n_results)
            for idx, doc_status in enumerate(random_doc_statuses):
                if doc_status.total_exp_results > n_results_list[idx] == min_result:
                    document = Document.query.filter_by(id=doc_status.doc_id).first()
                    turk_code = '%s_%s_%s' % (doc_status.doc_id, randomword(5), project.id)
                    doc_json = json.dumps(json.loads(document.doc_json))
                    return jsonify(dict(doc_json=doc_json,
                                        doc_status_id=doc_status.id,
                                        turk_code=turk_code,
                                        sanity_statement=document.sanity_statement,
                                        sanity_answer=document.sanity_answer
                                        ))
            return '', http.HTTPStatus.NOT_FOUND
    elif project_type.lower() == ProjectType.EVALUATION.value.lower():
        project = EvaluationProject.query.get(project_id)
        if not project:
            return '', http.HTTPStatus.NOT_FOUND
        else:
            for summ_status in project.summ_statuses:
                results = EvaluationResult.query.filter_by(
                    status_id=summ_status.id, is_filled=False).all()
                for result in results:
                    if result.opened_at:
                        delta = datetime.utcnow() - result.opened_at
                        if delta >= timedelta(minutes=3):
                            EvaluationResult.del_result(result)
            random_summ_statuses = list(project.summ_statuses)
            random.shuffle(random_summ_statuses)
            min_result = 999
            n_results_list = []
            for summ_status in random_summ_statuses:
                n_results = EvaluationResult.query.filter_by(status_id=summ_status.id).count()
                if n_results < min_result:
                    min_result = n_results
                n_results_list.append(n_results)
            for idx, summ_status in enumerate(random_summ_statuses):
                if summ_status.total_exp_results > n_results_list[idx] == min_result:
                    system_summary = Summary.query.get(summ_status.summary_id)
                    document = Document.query.filter_by(id=system_summary.doc_id).first()
                    system_text = system_summary.text
                    doc_json = json.loads(document.doc_json)
                    turk_code = '%s_%s_%s' % (system_summary.doc_id, randomword(5), project.id)
                    if project_category.lower() == ProjectCategory.INFORMATIVENESS_REF.value.lower():
                        ref_text = Summary.query.filter_by(id=summ_status.ref_summary_id).first().text
                        return jsonify(dict(system_text=system_text,
                                            ref_text=ref_text,
                                            summ_status_id=summ_status.id,
                                            sanity_statement=document.sanity_statement_2,
                                            sanity_answer=document.sanity_answer_2,
                                            turk_code=turk_code,
                                            ))
                    elif project_category.lower() == ProjectCategory.INFORMATIVENESS_DOC.value.lower():
                        return jsonify(dict(system_text=system_text,
                                            doc_json=doc_json,
                                            summ_status_id=summ_status.id,
                                            sanity_statement=document.sanity_statement,
                                            sanity_answer=document.sanity_answer,
                                            turk_code=turk_code
                                            ))
                    elif project_category.lower() == ProjectCategory.FLUENCY.value.lower():
                        return jsonify(dict(system_text=system_text,
                                            summ_status_id=summ_status.id,
                                            turk_code=turk_code,))
            return '', http.HTTPStatus.NOT_FOUND
    else:
        return '', http.HTTPStatus.BAD_REQUEST


@api.route('/project/<project_type>', methods=['POST'])
def api_project_create(project_type):
    if request.method == 'POST':
        data = request.get_json()
        project = None
        if project_type.lower() == ProjectType.ANNOTATION.value.lower():
            project = AnnotationProject.create_project(**data)
        elif project_type.lower() == ProjectType.EVALUATION.value.lower():
            project = EvaluationProject.create_project(**data)
        else:
            return '', http.HTTPStatus.BAD_REQUEST
        if project:
            return '', http.HTTPStatus.CREATED
        else:
            return '', http.HTTPStatus.CONFLICT


@api.route('/project/get/<project_type>/<project_name>', methods=['GET'])
def api_project_get(project_type, project_name):
    if project_type.lower() == ProjectType.ANNOTATION.value.lower():
        projects = AnnotationProject.query.filter_by(name=project_name).all()
    elif project_type.lower() == ProjectType.EVALUATION.value.lower():
        projects = EvaluationProject.query.filter_by(name=project_name).all()
    else:
        return '', http.HTTPStatus.BAD_REQUEST
    if len(projects) == 0:
        return '', http.HTTPStatus.NOT_FOUND
    else:
        result_json = {}
        for project in projects:
            result_json[project.id] = project.get_dict()
        return jsonify(result_json)


@api.route('/project/save_result/<project_type>', methods=['POST'])
def api_project_save_result(project_type):
    data = request.get_json()
    if project_type.lower() == ProjectType.ANNOTATION.value.lower():
        result = AnnotationResult.update_result(**data)
    elif project_type.lower() == ProjectType.EVALUATION.value.lower():
        result = EvaluationResult.update_result(**data)
    if result:
        return '', http.HTTPStatus.CREATED
    else:
        return '', http.HTTPStatus.CONFLICT


@api.route('/project/<project_id>/close', methods=['POST'])
def api_project_close(project_id):
    project = AnnotationProject.query.filter_by(id=project_id).first()
    if not project or project.is_active is False:
        return '', http.HTTPStatus.NOT_MODIFIED
    else:
        for doc_status in project.doc_statuses:
            results = AnnotationResult.query.filter_by(status_id=doc_status.id).all()
            results_json = {}
            for result in results:
                results_json[result.id] = json.loads(result.result_json)
            if len(results_json) != 0:
                Document.add_results(doc_status.doc_id, results_json)
                DocStatus.close(doc_status.id)
        AnnotationProject.deactivate(project_id)
        return '', http.HTTPStatus.OK


@api.route('/project/all_progress/<project_type>', methods=['GET'])
def api_project_progress_all(project_type):
    project_type = project_type.lower()
    if project_type == ProjectType.ANNOTATION.value.lower():
        projects = AnnotationProject.query.filter_by(is_active=True).all()
    elif project_type == ProjectType.EVALUATION.value.lower():
        projects = EvaluationProject.query.filter_by(is_active=True).all()
    else:
        return '', http.HTTPStatus.BAD_REQUEST

    if len(projects) == 0:
        return '', http.HTTPStatus.NOT_FOUND
    else:
        result_json = {'projects': []}
        for project in projects:
            project_json = project.to_dict()
            project_json['dataset_name'] = \
                Dataset.query.filter_by(id=project.dataset_id).first().name
            total_n_results = 0
            total_total_exp_results = 0
            if project_type == ProjectType.ANNOTATION.value.lower():
                for doc_status in project.doc_statuses:
                    n_results = AnnotationResult.query\
                        .filter_by(status_id=doc_status.id).count()
                    total_n_results += n_results
                    total_total_exp_results += doc_status.total_exp_results
            elif project_type == ProjectType.EVALUATION.value.lower():
                for summ_status in project.summ_statuses:
                    n_results = EvaluationResult.query\
                        .filter_by(status_id=summ_status.id).count()
                    total_n_results += n_results
                    total_total_exp_results += summ_status.total_exp_results
            project_json['progress'] = total_n_results/total_total_exp_results
            project_json['no'] = len(result_json['projects']) + 1
            if project_type.lower() == ProjectType.EVALUATION.value.lower():
                summ_group = SummaryGroup.query.get(project.summ_group_id)
                project_json['summ_group_name'] = summ_group.name

            category = project.category.lower()
            if project.category.lower() == ProjectCategory.INFORMATIVENESS_DOC.value.lower():
                highlight = 1
            else:
                highlight = 0
            if project.category.lower() == ProjectCategory.INFORMATIVENESS_DOC_NO.value.lower() or\
                    project.category.lower() == ProjectCategory.INFORMATIVENESS_DOC.value.lower():
                if project.category.lower() == ProjectCategory.INFORMATIVENESS_DOC_NO.value.lower():
                    category = ProjectCategory.INFORMATIVENESS_DOC.value.lower()
                project_json['link'] = urllib.parse.urljoin(
                request.host_url,
                '#/{type}/{category}/{highlight}/{id}/1'.format(
                    type=project_type,
                    highlight=highlight,
                    category=category,
                    id=project_json['id']
                    ))
            else:
                project_json['link'] = urllib.parse.urljoin(
                request.host_url,
                '#/{type}/{category}/{id}/1'.format(
                    type=project_type,
                    category=category,
                    id=project_json['id']
                ))
            result_json['projects'].append(project_json)
        return jsonify(result_json)


@api.route('/project/progress/<project_type>/<project_id>', methods=['GET'])
def api_project_progress(project_type, project_id):
    project_type = project_type.lower()
    if project_type == ProjectType.ANNOTATION.value.lower():
        project = AnnotationProject.query.get(project_id)
    elif project_type == ProjectType.EVALUATION.value.lower():
        project = EvaluationProject.query.get(project_id)
    else:
        return '', http.HTTPStatus.BAD_REQUEST
    if not project:
        return '', http.HTTPStatus.CONFLICT
    else:
        progress_json = None
        if project_type == ProjectType.ANNOTATION.value.lower():
            progress_json = {
                'documents': [],
                'name': ''
            }
        elif project_type == ProjectType.EVALUATION.value.lower():
            progress_json = {
                'systems': [],
                'name': '',
                'summ_group_name': ''
            }
        if project_type == ProjectType.ANNOTATION.value.lower():
            for doc_status in project.doc_statuses:
                document = Document.query.get(doc_status.doc_id)
                result_jsons = []
                for result in doc_status.results:
                    result_jsons.append(result.result_json)
                exp_results = doc_status.total_exp_results
                progress_json['documents'].append({
                    'no': len(progress_json['documents']) + 1,
                    'name': document.doc_id,
                    'progress': len(doc_status.results)/exp_results,
                    'result_jsons': result_jsons
                })
            progress_json['name'] = project.name
            return jsonify(progress_json)
        elif project_type == ProjectType.EVALUATION.value.lower():
            for summ_status in project.summ_statuses:
                result_jsons = []
                for result in summ_status.results:
                    result_jsons.append({
                        'precision': result.precision,
                        'recall': result.recall,
                        'clarity': result.clarity,
                        'fluency': result.fluency
                    })
                exp_results = summ_status.total_exp_results
                progress_json['systems'].append({
                    'no': len(progress_json['systems']) + 1,
                    'name': summ_status.summary_id,
                    'progress': len(summ_status.results) / exp_results,
                    'result_jsons': result_jsons
                })
            progress_json['name'] = project.name
            return jsonify(progress_json)
        else:
            return '', http.HTTPStatus.BAD_REQUEST


@api.route('/doc_status/progress/<doc_status_id>', methods=['GET'])
def api_doc_status_progress(doc_status_id):
    doc_status = DocStatus.query.filter_by(id=doc_status_id).first()
    if not doc_status:
        return '', http.HTTPStatus.NOT_FOUND
    n_results = len(AnnotationResult.query.filter_by(id=doc_status.id).all())
    progress = "{0:.2f}".format(n_results/doc_status.total_exp_results)
    return jsonify(dict(progress=progress))
