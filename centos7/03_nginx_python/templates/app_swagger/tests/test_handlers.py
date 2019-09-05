import pytest
import mock
import connexion
from gm_analytics import handlers


@pytest.fixture(scope='module')
def client():
    flask_app = connexion.FlaskApp(__name__)
    with flask_app.app.test_client() as c:
        yield c


@pytest.fixture
def user_info():
    return {'user_info': 'some_info'}


def test_get_health(client):
    # GIVEN ...
    # WHEN I access to the url ...
    # THEN ...
    response = client.get('/health')
    assert response.status_code == 200


def test_get_user_info(mocker, user_info):
    # GIVEN not query parameters or payload
    # WHEN I access to the url GET /users/daniel.barragan
    # THEN the information for an user must be returned
    mocker.patch.object(handlers, 'get_user_info', return_value=user_info)
    user_info = handlers.get_user_info('d4n13lbc')
    assert {'user_info': 'some_info'} == user_info

