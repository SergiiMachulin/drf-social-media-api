# Generated by Django 4.2 on 2023-04-23 12:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("userprofile", "0003_userprofile_first_name_userprofile_last_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="last_name",
        ),
    ]
