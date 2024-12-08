from django.db import models
from django.core.exceptions import ValidationError

class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    title = models.CharField(max_length=255)
    code = models.TextField()
    tests = models.TextField()
    description = models.TextField()
    hints = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    updated_on = models.DateTimeField(auto_now=True)  # Automatically set on update

    def __str__(self):
        return self.title

