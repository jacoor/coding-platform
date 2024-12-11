import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.models import Task, EducationPath  # Import EducationPath


@pytest.mark.django_db()
class TestTaskModel:
    def test_task_creation_with_education_path(self) -> None:  # Added return type annotation
        # Create an education path
        education_path = EducationPath.objects.create(
            name="Python Basics",
            description="Learn the fundamentals of Python.",
            ordering=1,
            difficulty="Easy",
        )

        # Create a task linked to the education path
        task = Task.objects.create(
            title="Sample Task",
            code="def add(a, b):\n    return a + b",
            tests="""import unittest

class TestAddFunction(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)
""",
            description="Implement the add function.",
            hints="Think about basic arithmetic operations.",
            difficulty="Easy",
            education_path=education_path,  # Set the relation
        )
        assert task.id is not None
        assert task.title == "Sample Task"
        assert task.education_path == education_path  # Verify the relation

    def test_task_string_representation(self) -> None:  # Added return type annotation
        education_path = EducationPath.objects.create(
            name="Advanced Python",
            description="Deep dive into Python.",
            ordering=2,
            difficulty="Medium",
        )
        task = Task(title="Sample Task", education_path=education_path)
        assert str(task) == "Sample Task"

    def test_code_field_validation(self) -> None:  # Added return type annotation
        education_path = EducationPath.objects.create(
            name="Web Development",
            description="Learn how to build web apps.",
            ordering=3,
            difficulty="Medium",
        )
        task = Task(
            title="Invalid Task",
            code="",  # Invalid code
            tests="",
            description="",
            difficulty="Easy",
            education_path=education_path,
        )
        # Explicitly trigger validation
        with pytest.raises(ValidationError):
            task.full_clean()

    def test_difficulty_choices(self) -> None:  # Added return type annotation
        education_path = EducationPath.objects.create(
            name="Data Science",
            description="Data analysis and machine learning.",
            ordering=4,
            difficulty="Hard",
        )
        task = Task(
            title="Medium Task",
            code="print('Hello, World!')",
            tests="import unittest",
            description="A medium difficulty task.",
            difficulty="Medium",
            education_path=education_path,
        )
        task.save()
        assert task.difficulty == "Medium"
        assert task.education_path == education_path

        # Test invalid difficulty
        task = Task(
            title="Invalid Difficulty Task",
            code="print('Hello, World!')",
            tests="import unittest",
            description="An invalid difficulty task.",
            difficulty="Unknown",  # Invalid difficulty
            education_path=education_path,
        )
        # Explicitly trigger validation
        with pytest.raises(ValidationError):
            task.full_clean()
