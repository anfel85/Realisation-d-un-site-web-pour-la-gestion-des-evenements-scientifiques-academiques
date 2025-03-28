# Generated by Django 5.0.3 on 2024-05-11 00:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_participation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='soumission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=30)),
                ('resume', models.TextField(max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('contrat', models.FileField(upload_to='documents/', verbose_name='PDF File')),
                ('attestation', models.FileField(upload_to='documents/', verbose_name='PDF File')),
                ('prestation', models.FileField(upload_to='documents/', verbose_name='PDF File')),
                ('evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.evénement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
