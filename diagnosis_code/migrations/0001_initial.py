# Generated by Django 4.0.4 on 2022-05-23 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosisCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category_code', models.CharField(max_length=50)),
                ('diagnosis_code', models.CharField(max_length=50)),
                ('full_code', models.CharField(max_length=50)),
                ('abbreviated_description', models.CharField(max_length=50)),
                ('full_description', models.CharField(max_length=800)),
                ('category_title', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]