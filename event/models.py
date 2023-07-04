from django.db import models

# Create your models here.


class OldpersonInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    id_card = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    img_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oldperson_info'



class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    old_id = models.CharField(primary_key=False, max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'event'