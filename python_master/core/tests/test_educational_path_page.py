import pytest
from django.test import Client
from django.urls import reverse

from core.models import EducationPath


@pytest.fixture()
def client() -> Client:
    return Client()


@pytest.fixture()
def create_education_paths():
    return [
        EducationPath.objects.create(
            name=f"Path {i}",
            description=f"Description for path {i}",
            ordering=i,
            difficulty="Easy" if i % 3 == 0 else "Medium" if i % 3 == 1 else "Hard",
        )
        for i in range(31)
    ]


@pytest.mark.django_db()
def test_education_path_list_first_page(client: Client, create_education_paths: list[EducationPath]) -> None:
    # Given
    url = reverse("education_path_list")

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 200
    assert "paths" in response.context
    assert len(response.context["paths"]) == 10  # Check if 10 paths are displayed per page
    for path in response.context["paths"]:
        assert hasattr(path, "name")
        assert hasattr(path, "description")
        assert hasattr(path, "difficulty")


@pytest.mark.django_db()
@pytest.mark.parametrize(("page", "expected_count"), [(2, 10), (3, 10), (4, 1)])
def test_education_path_list_pagination(client: Client, create_education_paths: list[EducationPath], page: int, expected_count: int) -> None:
    # Given
    url = reverse("education_path_list")

    # When
    response = client.get(f"{url}?page={page}")

    # Then
    assert response.status_code == 200
    assert "paths" in response.context
    assert len(response.context["paths"]) == expected_count  # Check if the correct number of paths are displayed per page


@pytest.mark.django_db()
def test_education_path_list_empty(client: Client) -> None:
    # Given
    url = reverse("education_path_list")

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 200
    assert "paths" in response.context
    assert len(response.context["paths"]) == 0  # Check if no paths are displayed when there are no paths in the database
