import pytest
from django.db import IntegrityError

from core.models import EducationPath  # Adjust 'myapp' to the actual app name


@pytest.mark.django_db()
def test_education_path_creation() -> None:
    path: EducationPath = EducationPath.objects.create(
        name="Introduction to Python",
        description="A beginner-friendly path to learn Python programming.",
        ordering=1,
        difficulty="Easy",
    )
    assert path.name == "Introduction to Python"
    assert path.description == "A beginner-friendly path to learn Python programming."
    assert path.ordering == 1
    assert path.difficulty == "Easy"


@pytest.mark.django_db()
def test_education_path_ordering() -> None:
    path1: EducationPath = EducationPath.objects.create(
        name="Introduction to Python",
        description="Learn the basics of Python.",
        ordering=2,
        difficulty="Easy",
    )
    path2: EducationPath = EducationPath.objects.create(
        name="Advanced Python",
        description="Advanced Python concepts.",
        ordering=1,
        difficulty="Hard",
    )
    paths: list[EducationPath] = list(EducationPath.objects.all().order_by("ordering"))
    assert paths == [path2, path1]


@pytest.mark.django_db()
def test_education_path_timestamps() -> None:
    from django.utils.timezone import now

    path: EducationPath = EducationPath.objects.create(
        name="Data Structures",
        description="Learn data structures for coding interviews.",
        ordering=1,
        difficulty="Medium",
    )
    assert path.created_at <= now()
    assert path.updated_at <= now()

    path.name = "Updated Data Structures"
    path.save()
    assert path.updated_at > path.created_at


@pytest.mark.django_db()
def test_education_path_unique_name() -> None:
    EducationPath.objects.create(
        name="Web Development",
        description="Learn to build web applications.",
        ordering=1,
        difficulty="Medium",
    )
    with pytest.raises(IntegrityError):
        EducationPath.objects.create(
            name="Web Development",
            description="Duplicate name should raise an error.",
            ordering=2,
            difficulty="Hard",
        )
