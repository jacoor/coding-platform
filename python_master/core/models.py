from typing import ClassVar

from django.db import models


class Task(models.Model):

    DIFFICULTY_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    title = models.CharField(max_length=255)
    code = models.TextField()
    tests = models.TextField()
    description = models.TextField()
    hints = models.TextField(blank=True)  # Removed null=True
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    updated_on = models.DateTimeField(auto_now=True)  # Automatically set on update

    def __str__(self) -> str:
        return self.title

class EducationPath(models.Model):
    DIFFICULTY_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    ordering = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
