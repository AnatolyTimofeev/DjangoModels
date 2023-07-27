# Generated by Django 4.2.3 on 2023-07-25 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turists', '0002_perevaladded_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='perevaladded',
            name='user',
            field=models.JSONField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perevaladded',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='new'),
        ),
    ]
