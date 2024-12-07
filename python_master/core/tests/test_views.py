import json
import pytest
from django.urls import reverse
from django.test import Client
from unittest.mock import patch


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def url():
    return reverse("submit")  # Ensure this matches your URL configuration


@patch("core.views.submit_code")
@patch("core.views.wait_for_result")
def test_submit_view_success(mock_wait_for_result, mock_submit_code, client, url):
    # Mock successful token generation and result retrieval
    mock_submit_code.return_value = "fake-token"
    mock_wait_for_result.return_value = {"status": {"description": "Accepted"}, "stdout": "Test output", "stderr": None}
    response = client.post(
        url,
        data=json.dumps({"code": 'print("Hello, World!")', "tests": "assert True"}),
        content_type="application/json",
    )
    # Assertions
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["result"]["status"] == "Accepted"
    assert response.json()["result"]["stdout"] == "Test output"
    assert response.json()["result"]["stderr"] is None


@patch("core.views.submit_code")
def test_submit_view_code_submission_failure(mock_submit_code, client, url):
    # Mock a failed token generation
    mock_submit_code.return_value = None
    response = client.post(
        url,
        data=json.dumps({"code": 'print("Hello, World!")', "tests": "assert True"}),
        content_type="application/json",
    )
    # Assertions
    assert response.status_code == 200
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Code submission failed"


def test_submit_view_invalid_json(client, url):
    response = client.post(url, data="not a json", content_type="application/json")
    # Assertions
    assert response.status_code == 400
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Invalid JSON"
