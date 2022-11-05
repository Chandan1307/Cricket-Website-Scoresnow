# Generated by Django 4.0.8 on 2022-11-01 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0002_match'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('city', models.ForeignKey(blank=True, help_text='Which city it belongs to.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='series.seriespage')),
            ],
            options={
                'verbose_name_plural': 'Stadium',
            },
        ),
    ]