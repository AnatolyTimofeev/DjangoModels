# Generated by Django 4.2.3 on 2023-07-15 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perevaladded',
            name='status',
            field=models.CharField(choices=[('1', 'new'), ('2', 'pending'), ('3', 'accepted'), ('4', 'rejected')], default='new'),
        ),
    ]
