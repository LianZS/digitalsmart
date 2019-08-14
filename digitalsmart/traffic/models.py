from django.db import models


class CityInfoManager(models.Model):
    pid = models.IntegerField(db_column="pid", verbose_name="城市标识")
    cityname = models.CharField(max_length=32, default=None, db_column="name", verbose_name="城市名")
    longitude = models.FloatField(db_column="longitude", verbose_name="城市经度")
    latitude = models.FloatField(db_column="latitude", verbose_name="城市维度")
    weatherpid = models.CharField(max_length=16, db_column="weatherpid", verbose_name="天气标识")
    yearpid = models.IntegerField(db_column="yearpid", verbose_name="城市季度交通标识")

    class Meta:
        db_table = "citymanager"


class CityTraffic(models.Model):
    pid = models.IntegerField(db_column="pid", verbose_name="城市标识")
    ddate = models.IntegerField(db_column="ddate", verbose_name="日期")
    ttime = models.TimeField(db_column="ttime", verbose_name="时间")
    rate = models.FloatField(db_column="rate", verbose_name="交通拥堵指数")

    class Meta:
        db_table = "citytraffic"
        index_together = ["pid", "ddate", "ttime", "rate"]


class RoadInfoManager(models.Model):
    citypid = models.IntegerField(db_column="pid", verbose_name="城市标识")
    cityname = models.CharField(max_length=32, default=None, db_column="name", verbose_name="城市名")  # 设计缺陷
    roadid = models.SmallIntegerField(db_column="roadid", verbose_name="道路标识")
    up_date = models.IntegerField(db_column="up_date", verbose_name="更新时间")

    class Meta:
        db_table = "roadmanager"


class RoadTraffic(models.Model):
    citypid = models.IntegerField(db_column="pid", verbose_name="城市标识")
    roadpid = models.SmallIntegerField(db_column="roadid", verbose_name="道路标识")
    roadname = models.CharField(max_length=80, db_column="roadname", verbose_name="路名")
    up_date = models.IntegerField(db_column="up_date", verbose_name="更新时间")
    speed = models.FloatField(db_column="speed", verbose_name="速度")
    direction = models.CharField(max_length=80, db_column="direction", verbose_name="方向")
    bounds = models.FileField(db_column="bound", verbose_name="道路经纬度数据集")
    data = models.FileField(db_column="data", verbose_name="道路交通数据集")

    rate = models.FloatField(db_column="rate", verbose_name="最近交通拥堵指数")

    class Meta:
        db_table = "roadtraffic"

        index_together = ["citypid", "up_date"]


class YearTraffic(models.Model):
    yearpid = models.IntegerField(db_column="pid", verbose_name="年度标识")
    tmp_date = models.IntegerField(db_column="tmp_date", verbose_name="日期")
    rate = models.FloatField(db_column="rate", verbose_name="交通指数")

    class Meta:
        db_table = "yeartraffic"
        index_together = ["yearpid", "tmp_date"]

class AirState(models.Model):
    citypid = models.IntegerField(db_column="pid", verbose_name="城市标识")
    flag=models.BooleanField(db_column="flag",verbose_name="判断是否为最新数据，1是，0否")
    aqi=models.SmallIntegerField(db_column="aqi",verbose_name="AQI ")
    lasttime=models.DateTimeField(db_column="lasttime",verbose_name="最近更新时间")
    pm2=models.SmallIntegerField(db_column="pm2",verbose_name="PM2.5/1h")
    pm10=models.SmallIntegerField(db_column="pm10",verbose_name="PM10/1h")
    co=models.FloatField(db_column="co",verbose_name="CO/1h")
    no2=models.SmallIntegerField(db_column="no2",verbose_name="NO2/1h")
    o3=models.SmallIntegerField(db_column="o3",verbose_name="O3/8h")
    so2=models.SmallIntegerField(db_column="so2",verbose_name="SO2/1h")
    class Meta:
        db_table="airstate"



