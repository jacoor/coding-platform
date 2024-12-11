import pytest
from django.core.exceptions import ValidationError

from core.models import EducationPath, Task  # Import EducationPath


@pytest.mark.django_db()
class TestTaskModel:
    def test_task_creation_with_multiple_education_paths(self) -> None:  # Added return type annotation
        # Create multiple education paths
        path1 = EducationPath.objects.create(
            name="Python Basics",
            description="Learn the fundamentals of Python.",
            ordering=1,
            difficulty="Easy",
        )
        path2 = EducationPath.objects.create(
            name="Web Development",
            description="Build web applications.",
            ordering=2,
            difficulty="Medium",
        )

        # Create a task linked to multiple education paths
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
        )
        task.education_paths.set([path1, path2])  # Set multiple paths
        task.save()

        assert task.id is not None
        assert task.title == "Sample Task"
        assert task.education_paths.count() == 2  # Verify multiple relations
        assert path1 in task.education_paths.all()
        assert path2 in task.education_paths.all()

    def test_task_string_representation(self) -> None:  # Added return type annotation
        task = Task(title="Sample Task")
        assert str(task) == "Sample Task"

    def test_code_field_validation(self) -> None:  # Added return type annotation
        task = Task(
            title="Invalid Task",
            code="",  # Invalid code
            tests="",
            description="",
            difficulty="Easy",
        )
        # Explicitly trigger validation
        with pytest.raises(ValidationError):
            task.full_clean()

    def test_difficulty_choices(self) -> None:  # Added return type annotation
        path = EducationPath.objects.create(
            name="Data Science",
            description="Data analysis and machine learning.",
            ordering=3,
            difficulty="Hard",
        )
        task = Task(
            title="Medium Task",
            code="print('Hello, World!')",
            tests="import unittest",
            description="A medium difficulty task.",
            difficulty="Medium",
        )
        task.save()
        task.education_paths.add(path)  # Associate with a path
        assert task.difficulty == "Medium"
        assert path in task.education_paths.all()

        # Test invalid difficulty
        task = Task(
            title="Invalid Difficulty Task",
            code="print('Hello, World!')",
            tests="import unittest",
            description="An invalid difficulty task.",
            difficulty="Unknown",  # Invalid difficulty
        )
        # Explicitly trigger validation
        with pytest.raises(ValidationError):
            task.full_clean()
