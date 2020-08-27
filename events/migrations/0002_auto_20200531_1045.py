# Generated by Django 3.0.6 on 2020-05-31 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamapplication',
            name='id',
        ),
        migrations.AlterField(
            model_name='teamapplication',
            name='participation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='events.Participation'),
        ),
    ]
