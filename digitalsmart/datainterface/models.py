from django.db import models


# Create your models here.
class PDFFile(models.Model):
    id = models.UUIDField(primary_key=True, db_column="id", verbose_name="用户提交时唯一产生uuid，用于下载文件的凭证", editable=False)
    file = models.FileField(upload_to="pdf", db_column="file")

    class Meta:
        db_table = "pdfdb"


class WeatherManager(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="id", verbose_name="地区唯一标识")
    city = models.CharField(max_length=32, db_column="city", verbose_name="城市名")

    class Meta:
        db_table = "weathermanager"


class WeatherDB(models.Model):
    pid = models.SmallIntegerField(db_column="pid", verbose_name="地区标识")
    ddate = models.IntegerField(db_column="ddate", verbose_name="日期")
    weatherstate = models.CharField(max_length=32, db_column="weatherstate", verbose_name="天气情况")
    template = models.CharField(max_length=32, db_column="template", verbose_name="温度")
    wind = models.CharField(max_length=32, db_column="wind", verbose_name="风力")

    class Meta:
        db_table = "weatherdb"
        index_together = ['pid', 'ddate']
