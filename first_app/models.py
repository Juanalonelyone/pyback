from django.db import models


# Create your models here.
class Admin(models.Model):
    admin_name = models.CharField(max_length=255, blank=True, null=True)
    admin_password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'admin'
