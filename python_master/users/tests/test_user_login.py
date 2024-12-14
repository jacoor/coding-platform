import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

User = get_user_model()


@pytest.fixture()
def admin_user(db) -> User:
    return User.objects.create_superuser(email="admin@example.com", password="adminpassword")  # nosec


@pytest.fixture()
def client() -> Client:
    return Client()


def test_admin_login(client: Client, admin_user: User) -> None:
    login_url = reverse("admin:login")
    response = client.post(login_url, {"username": admin_user.email, "password": "adminpassword"})
    assert response.status_code == 302  # Redirect to admin index page
    assert response.url == reverse("admin:index") or response.url == "/accounts/profile/"


def test_invalid_login(db, client: Client) -> None:
    login_url = reverse("admin:login")
    response = client.post(login_url, {"username": "invalid@example.com", "password": "wrongpassword"})
    assert response.status_code == 200  # Login page is re-rendered
    assert "Please enter the correct email and password" in response.content.decode()
