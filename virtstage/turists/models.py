from django.db import models

new = 'new'
pending ='pending'
accepted = 'accepted'
rejected = 'rejected'
CHOISE = [(new,'new'),(pending,'pending'),(accepted,'accepted'),(rejected,'rejected')]

class PerevalAdded(models.Model):
    status = models.CharField(default='new', choices=CHOISE)
    data_added = models.DateTimeField(auto_now_add=True)
    raw_data = models.JSONField()
    images = models.JSONField()
    class Meta:
        db_table = 'pereval_added'




