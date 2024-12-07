import pytest
from unittest.mock import patch, MagicMock
from ..utils import submit_code, get_submission_result, wait_for_result
from django.test import override_settings


# Test for submit_code function
@patch("requests.post")
def test_submit_code_success(mock_post):
    # Mock a successful response from Judge0
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"token": "fake-token"}
    mock_post.return_value = mock_response
    # Call the function
    token = submit_code('print("Hello, World!")')
    # Assertions
    assert token == "fake-token"
    mock_post.assert_called_once()


@patch("requests.post")
def test_submit_code_failure(mock_post):
    # Mock a failed response from Judge0
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    mock_post.return_value = mock_response
    # Call the function
    token = submit_code('print("Hello, World!")')
    # Assertions
    assert token is None
    mock_post.assert_called_once()


# Test for get_submission_result function
@patch("requests.get")
def test_get_submission_result_success(mock_get):
    # Mock a successful response from Judge0
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": {"description": "Accepted"}, "stdout": "Hello, World!"}
    mock_get.return_value = mock_response
    # Call the function
    result = get_submission_result("fake-token")
    # Assertions
    assert result["status"]["description"] == "Accepted"
    mock_get.assert_called_once()


@patch("requests.post")
@override_settings(JUDGE0={"API_URL": "http://fake-url", "HEADERS": {}, "DELAY": 1})
def test_submit_code_failure(mock_post):
    # Mock a failed response from Judge0
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    mock_post.return_value = mock_response
    # Assert that an exception is raised
    with pytest.raises(Exception) as excinfo:
        submit_code('print("Hello, World!")')
    assert "Error during submission" in str(excinfo.value)


@patch("requests.get")
def test_wait_for_result_success(mock_get):
    # Mock a successful response from Judge0
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": {"description": "Accepted"}, "stdout": "OK"}
    mock_get.return_value = mock_response
    # Call the function
    result = wait_for_result("fake-token", timeout=5)
    # Assertions
    assert result["status"]["description"] == "Accepted"
    mock_get.assert_called()


@patch("requests.get")
def test_wait_for_result_timeout(mock_get):
    # Mock a response that never reaches a terminal state
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": {"description": "Processing"}}
    mock_get.return_value = mock_response
    # Call the function
    result = wait_for_result("fake-token", timeout=1)
    # Assertions
    assert result is None
    mock_get.assert_called()
