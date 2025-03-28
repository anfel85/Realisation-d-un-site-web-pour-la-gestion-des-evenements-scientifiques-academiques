# Generated by Django 5.0.3 on 2024-04-29 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_rename_titre_evénement_nom_evnt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evénement',
            name='heure_debut_soumission',
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='evénement',
            name='heure_fin_enchere',
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='evénement',
            name='heure_fin_soumission',
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='evénement',
            name='heuree_debut_enchere',
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
    ]
