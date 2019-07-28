import json
import http
from backend.models import AnnotationProject, EvaluationProject,\
    ProjectCategory, ProjectType
from tests.fixture import init_db, test_client


def create_proj_resp(test_client, project_type, name, project_category=''):
    if project_type.lower() == ProjectType.ANNOTATION.value.lower():
        return test_client.post('/project/%s' % ProjectType.ANNOTATION.value,
                                data=json.dumps(dict(
                                    name=name,
                                    dataset_name='BBC_Sample',
                                    category=ProjectCategory.HIGHLIGHT.value,
                                    total_exp_results=3
                                    )
                                ),
                                content_type='application/json'
                                )
    elif project_type.lower() == ProjectType.EVALUATION.value.lower():
        if project_category.lower() == ProjectCategory.INFORMATIVENESS_DOC.value.lower():
            return test_client.post('/project/%s' % ProjectType.EVALUATION.value,
                                    data=json.dumps(dict(
                                        name=name,
                                        dataset_name='BBC_Sample',
                                        category=ProjectCategory.INFORMATIVENESS_DOC.value,
                                        total_exp_results=3,
                                        summ_group_name='BBC_Sample_ref_gold'
                                    )),
                                    content_type='application/json'
                                    )
        elif project_category.lower() == ProjectCategory.INFORMATIVENESS_REF.value.lower():
            return test_client.post('/project/%s' % ProjectType.EVALUATION.value,
                                    data=json.dumps(dict(
                                        name=name,
                                        dataset_name='BBC_Sample',
                                        category=ProjectCategory.INFORMATIVENESS_REF.value,
                                        total_exp_results=3,
                                        summ_group_name='BBC_Sample_ref_gold'
                                    )),
                                    content_type='application/json'
                                    )
        elif project_category.lower() == ProjectCategory.FLUENCY.value.lower():
            return test_client.post('/project/%s' % ProjectType.EVALUATION.value,
                                    data=json.dumps(dict(
                                        name=name,
                                        dataset_name='BBC_Sample',
                                        category=ProjectCategory.FLUENCY.value,
                                        total_exp_results=3,
                                        summ_group_name='BBC_Sample_ref_gold'
                                    )),
                                    content_type='application/json'
                                    )


def test_project_annotation_result(test_client, init_db):
    # Create project
    response = create_proj_resp(
        test_client,
        ProjectType.ANNOTATION.value,
        name='Test_Create_Result_Annotation'
    )
    assert response.status_code == http.HTTPStatus.CREATED
    # Get project
    response = test_client.get(
        '/project/get/annotation/%s' % 'Test_Create_Result_Annotation')
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.get_json()) > 0 is not None
    project_id = list(response.get_json().keys())[0]
    # Get document
    response = test_client.get(
        '/project/%s/%s/%s/single_doc' %
        (ProjectType.ANNOTATION.value, ProjectCategory.HIGHLIGHT.value, project_id))
    doc_status_id = response.get_json()['doc_status_id']
    # Post result
    annotation_result_json = {
        'project_id': project_id,
        'status_id': doc_status_id,
        'result_json': {
          'highlights': {},
          'components': [],
          'words': [],
        },
        'category': 'highlight',
        'validity': True,
        'email': 'test@test.com',
        'mturk_code': 'test123',
    }
    response = test_client.post('project/save_result/annotation',
                                data=json.dumps(annotation_result_json),
                                content_type='application/json')
    assert response.status_code == http.HTTPStatus.CREATED


def test_project_eval_inf_doc_result(test_client, init_db):
    # Create project
    response = create_proj_resp(
        test_client,
        ProjectType.EVALUATION.value,
        project_category=ProjectCategory.INFORMATIVENESS_DOC.value,
        name='Test_Create_Result_Evaluation_InfDoc'
    )
    assert response.status_code == http.HTTPStatus.CREATED
    # Get project
    response = test_client.get(
        '/project/get/evaluation/%s' % 'Test_Create_Result_Evaluation_InfDoc')
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.get_json()) > 0 is not None
    project_id = list(response.get_json().keys())[0]
    # Get document
    response = test_client.get(
        '/project/%s/%s/%s/single_doc' %
        (ProjectType.EVALUATION.value, ProjectCategory.INFORMATIVENESS_DOC.value, project_id))
    assert response.status_code == http.HTTPStatus.OK
    summ_status_id = response.get_json()['summ_status_id']
    # Post result
    evaluation_result_json = {
        'project_id': project_id,
        'status_id': summ_status_id,
        'precision': 1.0,
        'recall': 1.0,
        'category': ProjectCategory.INFORMATIVENESS_DOC.value,
        'validity': True,
        'email': 'test@test.com',
        'mturk_code': 'test123',
    }
    response = test_client.post('project/save_result/evaluation',
                                data=json.dumps(evaluation_result_json),
                                content_type='application/json')
    assert response.status_code == http.HTTPStatus.CREATED


def test_project_eval_inf_ref_result(test_client, init_db):
    # Create project
    response = create_proj_resp(
        test_client,
        ProjectType.EVALUATION.value,
        project_category=ProjectCategory.INFORMATIVENESS_REF.value,
        name='Test_Create_Result_Evaluation_InfRef'
    )
    assert response.status_code == http.HTTPStatus.CREATED
    # Get project
    response = test_client.get(
        '/project/get/evaluation/%s' % 'Test_Create_Result_Evaluation_InfRef')
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.get_json()) > 0 is not None
    project_id = list(response.get_json().keys())[0]
    # Get document
    response = test_client.get(
        '/project/%s/%s/%s/single_doc' %
        (ProjectType.EVALUATION.value, ProjectCategory.INFORMATIVENESS_REF.value, project_id))
    assert response.status_code == http.HTTPStatus.OK
    summ_status_id = response.get_json()['summ_status_id']
    # Post result
    evaluation_result_json = {
        'project_id': project_id,
        'status_id': summ_status_id,
        'precision': 1.0,
        'recall': 1.0,
        'category': ProjectCategory.INFORMATIVENESS_REF.value,
        'validity': True,
        'email': 'test@test.com',
        'mturk_code': 'test123',
    }
    response = test_client.post('project/save_result/evaluation',
                                data=json.dumps(evaluation_result_json),
                                content_type='application/json')
    assert response.status_code == http.HTTPStatus.CREATED


# def test_project_eval_fluency_result(test_client, init_db):
#     # Create project
#     response = create_proj_resp(
#         test_client,
#         ProjectType.EVALUATION.value,
#         project_category=ProjectCategory.FLUENCY.value,
#         name='Test_Create_Result_Evaluation_Fluency'
#     )
#     assert response.status_code == http.HTTPStatus.CREATED
#     # Get project
#     response = test_client.get(
#         '/project/get/evaluation/%s' % 'Test_Create_Result_Evaluation_Fluency')
#     assert response.status_code == http.HTTPStatus.OK
#     assert len(response.get_json()) > 0 is not None
#     project_id = list(response.get_json().keys())[0]
#     # Get document
#     response = test_client.get(
#         '/project/%s/%s/%s/single_doc' %
#         (ProjectType.EVALUATION.value, ProjectCategory.FLUENCY.value, project_id))
#     assert response.status_code == http.HTTPStatus.OK
#     summ_status_id = response.get_json()['summ_status_id']
#     # Post result
#     evaluation_result_json = {
#         'project_id': project_id,
#         'status_id': summ_status_id,
#         'fluency': 1.0,
#         'clarity': 1.0,
#         'category': ProjectCategory.FLUENCY.value,
#     }
#     response = test_client.post('project/save_result/evaluation',
#                                 data=json.dumps(evaluation_result_json),
#                                 content_type='application/json')
#     assert response.status_code == http.HTTPStatus.CREATED


def test_project_create_annotation(test_client, init_db):
    # Test Annotation Project
    response = create_proj_resp(
        test_client,
        ProjectType.ANNOTATION.value,
        name='Test_Create_Annotation'
    )
    assert response.status_code == http.HTTPStatus.CREATED
    project = AnnotationProject.query.filter_by(name='Test_Create_Annotation').first()
    assert project is not None


def test_project_create_evaluation(test_client, init_db):
    # Test Evaluation Project
    response = create_proj_resp(
        test_client,
        ProjectType.EVALUATION.value,
        project_category=ProjectCategory.INFORMATIVENESS_DOC.value,
        name='Test_Create_Evaluation_Doc'
    )
    assert response.status_code == http.HTTPStatus.CREATED
    project = EvaluationProject.query.filter_by(name='Test_Create_Evaluation_Doc').first()
    assert project is not None

    response = create_proj_resp(
        test_client,
        ProjectType.EVALUATION.value,
        project_category=ProjectCategory.INFORMATIVENESS_REF.value,
        name='Test_Create_Evaluation_Ref'
    )
    assert response.status_code == http.HTTPStatus.CREATED
    project = EvaluationProject.query.filter_by(name='Test_Create_Evaluation_Ref').first()
    assert project is not None


def test_project_get_all_progress_annotation(test_client, init_db):
    create_proj_resp(test_client, ProjectType.ANNOTATION.value, 'Test_Progress_All_Annotation')
    response = test_client.get('/project/all_progress/annotation')
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.get_json()['projects']) > 0
    assert response.get_json()['projects'][0]['dataset_name'] == 'BBC_Sample'
    assert 'progress' in response.get_json()['projects'][0]


def test_project_get_all_progress_evaluation(test_client, init_db):
    create_proj_resp(test_client, ProjectType.EVALUATION.value,
                     'Test_Progress_All_Evaluation', ProjectCategory.INFORMATIVENESS_REF.value)
    response = test_client.get('/project/all_progress/evaluation')
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.get_json()['projects']) > 0
    assert response.get_json()['projects'][0]['dataset_name'] == 'BBC_Sample'
    assert 'progress' in response.get_json()['projects'][0]


def test_project_get_single_unfinished_doc_annotation(test_client, init_db):
    create_proj_resp(test_client, ProjectType.ANNOTATION.value, 'Test_Single_Annotation')
    project = AnnotationProject.query.filter_by(name='Test_Single_Annotation').first()
    response = test_client.get(
        '/project/%s/%s/%s/single_doc' %
        (ProjectType.ANNOTATION.value, ProjectCategory.HIGHLIGHT, project.id))
    assert response.status_code == http.HTTPStatus.OK


def test_project_get_single_unfinished_summ_evaluation(test_client, init_db):
    create_proj_resp(test_client, ProjectType.EVALUATION.value,
                     name='Test_Single_Evaluation_Doc',
                     project_category=ProjectCategory.INFORMATIVENESS_DOC.value)
    project = EvaluationProject.query.filter_by(name='Test_Single_Evaluation_Doc').first()
    response = test_client.get(
        '/project/%s/%s/%s/single_doc' %
        (ProjectType.EVALUATION.value, ProjectCategory.INFORMATIVENESS_DOC.value, project.id)
    )
    assert response.status_code == http.HTTPStatus.OK

    create_proj_resp(test_client, ProjectType.EVALUATION.value,
                     name='Test_Single_Evaluation_Ref',
                     project_category=ProjectCategory.INFORMATIVENESS_REF.value)
    project = EvaluationProject.query.filter_by(name='Test_Single_Evaluation_Ref').first()
    response = test_client.get(
        '/project/%s/%s/%s/single_doc' %
        (ProjectType.EVALUATION.value, ProjectCategory.INFORMATIVENESS_REF.value, project.id)
    )
    assert response.status_code == http.HTTPStatus.OK


def test_doc_status(test_client, init_db):
    response = create_proj_resp(
        test_client,
        ProjectType.ANNOTATION.value,
        project_category=ProjectCategory.HIGHLIGHT.value,
        name='Test_Doc_Status'
    )
    assert response.status_code == http.HTTPStatus.CREATED
    response = test_client.get(
        '/project/get/annotation/%s' % 'Test_Doc_Status')
    assert len(response.get_json()) > 0
    project_id = list(response.get_json().keys())[0]
    response = test_client.get('/doc_status/progress/%s' % project_id)
    assert response.get_json()['progress'] == '0.00'


def test_project_get_progress_annotation(test_client, init_db):
    response = create_proj_resp(test_client, ProjectType.ANNOTATION.value, 'Test_Progress_Annotation')
    assert response.status_code == http.HTTPStatus.CREATED
    project = AnnotationProject.query.filter_by(name='Test_Progress_Annotation').first()
    response = test_client.get('/project/progress/annotation/%s' % project.id)
    assert response.status_code == http.HTTPStatus.OK
    assert 'documents' in response.get_json()
    assert len(response.get_json()['documents']) > 0


def test_project_get_progress_evaluation(test_client, init_db):
    response = create_proj_resp(test_client, ProjectType.EVALUATION.value,
                                project_category=ProjectCategory.INFORMATIVENESS_DOC.value,
                                name='Test_Progress_Evaluation')
    assert response.status_code == http.HTTPStatus.CREATED
    project = EvaluationProject.query.filter_by(name='Test_Progress_Evaluation').first()
    response = test_client.get('/project/progress/evaluation/%s' % project.id)
    assert response.status_code == http.HTTPStatus.OK
    assert 'systems' in response.get_json()
    assert len(response.get_json()['systems']) > 0
