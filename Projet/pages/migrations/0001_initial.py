# Generated by Django 5.0.3 on 2024-04-26 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evénement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=30)),
                ('acronym', models.CharField(max_length=30)),
                ('type', models.CharField(blank=True, choices=[('Séminaire', 'Séminaire'), ('Stand', 'Stand'), ('Symposium', 'Symposium'), ('Colloque', 'Colloque'), ('Congrès', 'Congrès'), ('Convention', 'Convention'), ('Atelier', 'Atelier'), ('Journée détude', 'Journée détude'), ('Conférence', 'Conférence')], max_length=30, null=True)),
                ('lieu', models.CharField(max_length=30)),
                ('date', models.CharField(max_length=30)),
            ],
        ),
    ]
