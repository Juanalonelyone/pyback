from django.db import models


# Create your models here.
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
        managed = True
        db_table = 'cap'
