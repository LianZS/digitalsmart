from django.db import models


# Create your models here.
class CityManager(models.Model):
    pid = models.SmallIntegerField(db_column="pid", verbose_name="标识")
    name = models.CharField(max_length=32, db_column="name", verbose_name="城市名字")
    longitude = models.FloatField(db_column="longitude", verbose_name="中心经度")
    latitude = models.FloatField(db_column="latitude", verbose_name="中心纬度")
    weatherpid = models.CharField(max_length=16, db_column="weatherpid", verbose_name="城市区域所对应的天气标识")
    yearpid = models.IntegerField(db_column="yearpid", verbose_name="年度交通标识")

    class Meta:
        db_table = "citymanager"


class CityTraffic(models.Model):
    pid = models.SmallIntegerField(db_column="pid", verbose_name="标识")
    ddate = models.IntegerField(db_column="ddate", verbose_name="日期,格式为yyyymmdd")
    ttime = models.TimeField(db_column="ttime", verbose_name="时间,格式为HH：MM：SS")
    rate = models.FloatField(db_column="rate", verbose_name="指数")

    class Meta:
        db_table = "citytraffic"
        unique_together = [['pid', 'ddate', 'ttime', 'rate']]


class RoadTraffic(models.Model):
    pid = models.SmallIntegerField(db_column="pid", verbose_name="标识")
    roadname = models.CharField(max_length=80, db_column="roadname", verbose_name="路名")
    up_date = models.IntegerField(db_column="up_date", verbose_name="更新时间，内容为时间戳")
    speed = models.FloatField(db_column="speed", verbose_name="速度")
    direction = models.CharField(max_length=80, db_column="direction", verbose_name="方向")
    bound = models.TextField(db_column="bound", verbose_name="经纬度列表字符串")
    data = models.TextField(db_column="data", verbose_name="指数集")
    roadid = models.SmallIntegerField(db_column="roadid",verbose_name="道路标识")
    class Meta:
        db_table = "roadtraffic"
        unique_together = [['pid', 'up_date']]


class YearTraffic(models.Model):
    pid = models.SmallIntegerField(db_column="pid", verbose_name="年度标识")
    tmp_date = models.IntegerField(db_column="tmp_date", verbose_name="日期,格式为yyyymmdd")
    rate = models.FloatField(db_column="rate", verbose_name="指数")

    class Meta:
        db_table = "yeartraffic"
        unique_together = [['pid', 'tmp_date']]
