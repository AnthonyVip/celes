from fastapi.testclient import TestClient
import pytest
from fastapi import status

from main import app
from core.settings import settings
from modules.token import Token


client = TestClient(app)


cls_token = Token()


@pytest.fixture
def mock_settings():
    class MockSettings:
        fire_base_api_key = settings.fire_base_api_key
    return MockSettings()


@pytest.fixture
def mock_user_request():
    class UserRequest:
        email = settings.email_test
        password = settings.pass_test
    return UserRequest()


@pytest.fixture
def mock_period_request():
    class PeriodRequest:
        start_date = "2023-01-01"
        end_date = "2023-12-31"

    return PeriodRequest()


@pytest.fixture
def mock_peridod_response():
    return ["cantidad", "total"]


@pytest.fixture
def mock_avg_response():
    return ["average_sales", "total_sales"]


@pytest.fixture
def mock_token_service():
    class MockTokenService:
        def create_access_token(self):
            token = cls_token.create_access_token({
                "email": settings.email_test,
                "id": "123"
            })

            return {"Authorization": f"Bearer {token}"}

    return MockTokenService().create_access_token()


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Service": "Celes!"}


def test_login_success(mock_user_request):
    body = {
        "email": mock_user_request.email,
        "password": mock_user_request.password
    }

    response = client.post("/users/login", json=body)

    assert response.status_code == status.HTTP_200_OK
    assert "jwt_token" in response.json()


def test_login_incorrect_credentials(mocker, mock_settings, mock_user_request):
    mock_post = mocker.patch('routes.auth.requests.post')
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {
        "error": ['Incorrect username or password']
    }
    mocker.patch('routes.auth.settings', mock_settings)

    response = client.post("/users/login", json={
        "email": mock_user_request.email,
        "password": mock_user_request.password
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"errors": ['Incorrect username or password']}


def test_sales_period_by_employee_success(
    mock_token_service,
    mock_period_request,
    mock_peridod_response
):
    headers = mock_token_service
    response = client.post("/datamart/sales_period_by_employee", json={
        "start_date": mock_period_request.start_date,
        "end_date": mock_period_request.end_date,
        "key_employee": "1|343"
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert all(i in response.json() for i in mock_peridod_response)


def test_sales_period_by_employee_not_found(
    mock_token_service,
    mock_period_request
):
    headers = mock_token_service
    response = client.post("/datamart/sales_period_by_employee", json={
        "start_date": mock_period_request.start_date,
        "end_date": mock_period_request.end_date,
        "key_employee": "1|"
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_sales_period_by_product_success(
    mock_token_service,
    mock_period_request,
    mock_peridod_response
):
    headers = mock_token_service
    response = client.post("/datamart/sales_period_by_product", json={
        "start_date": mock_period_request.start_date,
        "end_date": mock_period_request.end_date,
        "key_product": "1|44733"
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert all(i in response.json() for i in mock_peridod_response)


def test_sales_period_by_product_not_found(
    mock_token_service,
    mock_period_request
):
    headers = mock_token_service
    response = client.post("/datamart/sales_period_by_product", json={
        "start_date": mock_period_request.start_date,
        "end_date": mock_period_request.end_date,
        "key_product": "1|"
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_sales_period_by_store_success(
    mock_token_service,
    mock_period_request,
    mock_peridod_response
):
    headers = mock_token_service
    response = client.post("/datamart/sales_period_by_store", json={
        "start_date": mock_period_request.start_date,
        "end_date": mock_period_request.end_date,
        "key_store": "1|023"
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert all(i in response.json() for i in mock_peridod_response)


def test_sales_period_by_store_not_found(
    mock_token_service,
    mock_period_request
):
    headers = mock_token_service
    response = client.post("/datamart/sales_period_by_store", json={
        "start_date": mock_period_request.start_date,
        "end_date": mock_period_request.end_date,
        "key_store": "1|"
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_avg_sales_by_employee_success(
    mock_token_service,
    mock_avg_response
):
    headers = mock_token_service
    response = client.post("/datamart/avg_sales_by_employee", json={
        "key_employee": "1|343"
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert all(i in response.json() for i in mock_avg_response)


def test_avg_sales_by_employee_not_found(
    mock_token_service,
):
    headers = mock_token_service
    response = client.post("/datamart/avg_sales_by_employee", json={
        "key_employee": "1|"
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_avg_sales_by_product_success(
    mock_token_service,
    mock_avg_response
):
    headers = mock_token_service
    response = client.post("/datamart/avg_sales_by_product", json={
        "key_product": "1|44733"
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert all(i in response.json() for i in mock_avg_response)


def test_avg_sales_by_product_not_found(
    mock_token_service,
):
    headers = mock_token_service
    response = client.post("/datamart/avg_sales_by_product", json={
        "key_product": "1|"
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_avg_sales_by_store_success(
    mock_token_service,
    mock_avg_response
):
    headers = mock_token_service
    response = client.post("/datamart/avg_sales_by_store", json={
        "key_store": "1|023"
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert all(i in response.json() for i in mock_avg_response)


def test_avg_sales_by_store_not_found(
    mock_token_service,
):
    headers = mock_token_service
    response = client.post("/datamart/avg_sales_by_store", json={
        "key_store": "1|"
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
