# Generated by Django 5.1.4 on 2024-12-11 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_educationpath"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="education_paths",
            field=models.ManyToManyField(related_name="tasks", to="core.educationpath"),
        ),
    ]
