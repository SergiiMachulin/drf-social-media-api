# Generated by Django 4.2 on 2023-04-23 16:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="hashtags",
        ),
        migrations.DeleteModel(
            name="Hashtag",
        ),
        migrations.AddField(
            model_name="post",
            name="hashtags",
            field=models.CharField(
                blank=True, default=None, max_length=3000, null=True
            ),
        ),
    ]