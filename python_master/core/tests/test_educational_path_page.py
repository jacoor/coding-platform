import pytest
from django.urls import reverse
from django.test import Client
from core.models import EducationPath

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def create_education_paths():
    paths = [
        EducationPath.objects.create(
            name=f"Path {i}",
            description=f"Description for path {i}",
            ordering=i,
            difficulty="Easy" if i % 3 == 0 else "Medium" if i % 3 == 1 else "Hard"
        )
        for i in range(1, 31)
    ]
    return paths

@pytest.mark.django_db
def test_education_path_list_first_page(client, create_education_paths):
    # Given
    url = reverse('education_path_list')

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 200
    assert 'paths' in response.context
    assert len(response.context['paths']) == 10  # Check if 10 paths are displayed per page
    for path in response.context['paths']:
        assert 'name' in path
        assert 'description' in path
        assert 'difficulty' in path

@pytest.mark.django_db
@pytest.mark.parametrize("page, expected_count", [(2, 10), (3, 10), (4, 1)])
def test_education_path_list_pagination(client, create_education_paths, page, expected_count):
    # Given
    url = reverse('education_path_list')

    # When
    response = client.get(f"{url}?page={page}")

    # Then
    assert response.status_code == 200
    assert 'paths' in response.context
    assert len(response.context['paths']) == expected_count  # Check if the correct number of paths are displayed per page

@pytest.mark.django_db
def test_education_path_list_invalid_page(client, create_education_paths):
    # Given
    url = reverse('education_path_list')

    # When
    response = client.get(f"{url}?page=999")

    # Then
    assert response.status_code == 200
    assert 'paths' in response.context
    assert len(response.context['paths']) == 0  # Check if no paths are displayed for an invalid page

@pytest.mark.django_db
def test_education_path_list_empty(client):
    # Given
    url = reverse('education_path_list')

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 200
    assert 'paths' in response.context
    assert len(response.context['paths']) == 0  # Check if no paths are displayed when there are no paths in the database