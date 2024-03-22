# test_signup.py

from unittest.mock import patch
import pytest

import importlib.util


@pytest.fixture
def client():
    # Load api.py as a module
    spec = importlib.util.spec_from_file_location("api", "./api.py")
    api = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(api)

    # Access the app object from api.py
    app = api.app

    # Create a test client using the app
    with app.test_client() as client:
        # Yield the test client to the test case
        yield client


@pytest.fixture
def mock_send_email():
    with patch('app.utils.misc.send_email') as mock_send_email:
        yield mock_send_email


def test_signup_with_successful_email(mock_send_email, client):
    valid_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "Test1234@"
    }

    # Mock the send_email function to return True (simulating successful email sending)
    mock_send_email.return_value = True

    # Make POST request to signup route with valid data
    with patch('random.randint', return_value=123456):
        response = client.post('/user/signup', json=valid_data)

    # Check response status code
    assert response.status_code == 200

    # Check response content
    data = response.json
    assert data['ack'] == True

    # Check if send_email function was called with the expected arguments
    # Replace 'XXXXXX' with the expected verification code
    mock_send_email.assert_called_once_with(
        valid_data['email'], 'Verify Your Registration', 'Verification Code: 123456')


def test_signup_with_failed_email(mock_send_email, client):
    valid_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "Test1234@"
    }

    # Mock the send_email function to return False (simulating failed email sending)
    mock_send_email.return_value = False

    # Make POST request to signup route with valid data
    with patch('random.randint', return_value=123456):
        response = client.post('/user/signup', json=valid_data)

    # Check response status code
    assert response.status_code == 200

    # Check response content
    data = response.json
    print(data)
    assert data['ack'] == False

    # Check if send_email function was called with the expected arguments
    # Replace 'XXXXXX' with the expected verification code
    mock_send_email.assert_called_once_with(
        valid_data['email'], 'Verify Your Registration', 'Verification Code: 123456')
