import json
from tests.fixture import init_db, test_client


def test_get_dataset_list(test_client, init_db):
    response = test_client.get('/dataset')
    assert response.status_code == 200
    assert response.get_json()['names'] == ['BBC_Sample']


def test_get_json(test_client, init_db):
    response = test_client.get('/dataset/BBC_Sample')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'BBC_Sample'
