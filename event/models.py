# from django.db import models
#
# # Create your models here.
#
#
# class Event(models.Model):
#     old = models.ForeignKey('OldpersonInfo', models.DO_NOTHING, blank=True, null=True)
#     location = models.CharField(max_length=255, blank=True, null=True)
#     time = models.CharField(max_length=255, blank=True, null=True)
#     desc = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'event'