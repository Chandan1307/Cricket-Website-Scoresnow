# Generated by Django 4.1.2 on 2022-10-10 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_homepage_banner_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="body",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
