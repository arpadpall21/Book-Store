import re

import pytest
from fastapi.testclient import TestClient

from server import app, database, fill_db_with_fake_books

test_user = {
    'email': 'some_test@email.com',
    'password': 'some_password',
}


def get_session_id(response):
    cookie = response.headers['set-cookie']
    return re.search('sessionId=(.+?);', cookie).group(1)


@pytest.fixture
def client():
    database.connect()
    fill_db_with_fake_books(database)

    yield TestClient(app)
    database.disconnect()


def test_register_user_profile(client):
    response = client.post('profile/register', json=test_user)

    assert response.status_code == 201
    assert response.json() == {'success': True, 'message': 'user created'}


def test_login_and_logout_user(client):
    client.post('profile/register', json=test_user)
    login_response = client.post('profile/login', json=test_user)
    session_id = get_session_id(login_response)

    logout_response = client.get('profile/logout', headers={'sessionId': session_id})

    assert logout_response.status_code == 200
    assert logout_response.json() == {'success': True, 'message': 'user successfully logged out'}


def test_delete_user_profile(client):
    client.post('profile/register', json=test_user)
    login_response = client.post('profile/login', json=test_user)
    session_id = get_session_id(login_response)

    delelete_profile_response = client.delete('profile/delete', headers={'sessionId': session_id})

    assert delelete_profile_response.status_code == 200
    assert delelete_profile_response.json() == {'success': True, 'message': 'account deleted'}
