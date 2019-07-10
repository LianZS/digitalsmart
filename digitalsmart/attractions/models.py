from django.db import models

# Create your models here.

class Scenceflow(models.Model):
    name = models.CharField(max_length=64)
    scenceid = models.IntegerField()
    datetime = models.DateTimeField()
    num = models.IntegerField()
    class Meta:
        db_table = "scenceflow"
        unique_together=[['scenceid','datetime','num']]
