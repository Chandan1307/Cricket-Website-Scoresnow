# Generated by Django 4.0.8 on 2022-11-04 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0005_match_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='stadium',
            name='key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
