from django.db import models

# Create your models here.


class Worker(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    workername = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    id_card = models.CharField(max_length=255, blank=True, null=True)
    img_url = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'worker'

