# Generated by Django 5.1.5 on 2025-01-17 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_alter_appuser_password"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appuser",
            name="isSuperuser",
        ),
    ]