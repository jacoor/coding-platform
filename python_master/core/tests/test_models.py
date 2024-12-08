import pytest
from django.utils import timezone
from django.core.exceptions import ValidationError
from core.models import Task  # Replace 'myapp' with your app name

@pytest.mark.django_db
class TestTaskModel:

    def test_task_creation(self):
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
        assert task.id is not None
        assert task.title == "Sample Task"
        assert task.code.startswith("def add")
        assert task.tests.startswith("import unittest")
        assert task.description == "Implement the add function."
        assert task.hints == "Think about basic arithmetic operations."
        assert task.difficulty == "Easy"
        assert task.created_at <= timezone.now()

    def test_task_string_representation(self):
        task = Task(title="Sample Task")
        assert str(task) == "Sample Task"

    def test_code_field_validation(self):
        with pytest.raises(ValidationError):
            task = Task(
                title="Invalid Task",
                code="",
                tests="",
                description="",
                difficulty="Easy",
            )
            task.full_clean()

    def test_difficulty_choices(self):
        task = Task(
            title="Medium Task",
            code="print('Hello, World!')",
            tests="import unittest",
            description="A medium difficulty task.",
            difficulty="Medium",
        )
        task.save()
        assert task.difficulty == "Medium"

        # Test invalid difficulty
        with pytest.raises(ValidationError):
            task = Task(
                title="Invalid Difficulty Task",
                code="print('Hello, World!')",
                tests="import unittest",
                description="An invalid difficulty task.",
                difficulty="Unknown",
            )
            task.full_clean()