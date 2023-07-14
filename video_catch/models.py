from django.db import models

# Create your models here.
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
    old = models.ForeignKey('OldpersonInfo', models.DO_NOTHING, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    img_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event'

class Cap(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    has_face = models.CharField(max_length=255, blank=True, null=True)
    has_fall = models.CharField(max_length=255, blank=True, null=True)
    has_fire = models.CharField(max_length=255, blank=True, null=True)
    has_violence = models.CharField(max_length=255, blank=True, null=True)
    has_emotion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cap'
