# Generated by Django 4.2.3 on 2023-07-26 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turists', '0003_perevaladded_user_alter_perevaladded_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='perevaladded',
            name='user_email',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
    ]
