from django.db import models


# Create your models here.

class ScenceManager(models.Model):
    """
    信息概况总表
    """
    pid = models.SmallIntegerField(verbose_name="标识")
    area = models.CharField(max_length=32, verbose_name="地名")
    longitude = models.FloatField(verbose_name="中心经度")
    latitude = models.FloatField(verbose_name="中心纬度")
    province = models.CharField(max_length=18, verbose_name="省份")
    loaction = models.CharField(max_length=18, verbose_name="所处城市")
    citypid = models.IntegerField(verbose_name="所处城市标识")
    weatherpid = models.TextField(verbose_name="对应的天气标识")
    flag = models.SmallIntegerField(verbose_name="类别标识,百度数据为1，腾讯为0")

    class Meta:
        db_table = "scencemanager"
# class  ScenceFlow_Manager(models.Manager):
#     def get_queryset(self):
#         pass

class ScenceFlow(models.Model):
    """
    地区实时客流量数据
    """
    pid = models.SmallIntegerField(verbose_name="标识")
    ddate = models.IntegerField(verbose_name="日期,格式为yyyymmdd")
    ttime = models.TimeField(verbose_name="时间,格式为HH：MM：SS")
    num = models.IntegerField(verbose_name="总人数")

    def __str__(self):
        return "标识：{0}，日期：{1}，时间：{2}，数量：{3}".format(self.pid, self.ddate, self.ttime, self.num)

    class Meta:
        db_table = "scenceflow"
        unique_together = [['pid', 'ddate', 'ttime', 'num']]


class SearchRate(models.Model):
    """
    地名搜索频率
    """
    pid = models.SmallIntegerField(db_index=True, verbose_name="标识")
    tmp_date = models.IntegerField(verbose_name="时间,格式为yyyymmdd")
    area = models.CharField(max_length=32, verbose_name="地名")
    rate = models.IntegerField(verbose_name="频率")
    name = models.CharField(max_length=16, verbose_name="搜索引擎，包括微信-wechat，百度-baidu，搜狗-sougou")

    class Meta:
        db_table = "searchrate"


class Geographic(models.Model):
    """
    地区范围经纬度

    """
    pid = models.SmallIntegerField(db_index=True, verbose_name="标识")
    latitude = models.FloatField(verbose_name="中心纬度")
    loaction = models.CharField(max_length=18, verbose_name="所处城市")

    class Meta:
        db_table = "geographic"


class ScenceTrend(models.Model):
    """
    地区人口趋势

    """
    pid = models.SmallIntegerField(verbose_name="标识")
    ddate = models.IntegerField(verbose_name="日期,格式为yyyymmdd")
    ttime = models.TimeField(verbose_name="时间,格式为HH：MM：SS")
    rate = models.FloatField(verbose_name="频率")

    class Meta:
        db_table = "scencetrend"
        unique_together = [['pid', 'ddate', 'ttime', 'rate']]


class TableManager(models.Model):
    pid = models.SmallIntegerField(verbose_name="标识")
    area = models.CharField(max_length=32, verbose_name="地名")
    last_date = models.IntegerField(verbose_name="最近更新时间,根据最新时间查找数据")
    table_id = models.SmallIntegerField(verbose_name="对应表格标识，表格标识为0-9")

    class Meta:
        db_table = "tablemanager"


class PeoplePositionN(models.Model):
    """
    人口分布分表父类

    """
    pid = models.SmallIntegerField(verbose_name="标识")
    area = models.CharField(max_length=32, verbose_name="地名")
    lon = models.FloatField(verbose_name="经度")
    lat = models.FloatField(verbose_name="纬度")
    num = models.SmallIntegerField(verbose_name="人数")

    class Meta:
        abstract = True
        unique_together = [['pid', 'tmp_date']]


class PeoplePosition0(PeoplePositionN):
    class Meta:
        db_table = "peopleposition0"


class PeoplePosition1(PeoplePositionN):
    class Meta:
        db_table = "peopleposition1"


class PeoplePosition2(PeoplePositionN):
    class Meta:
        db_table = "peopleposition2"


class PeoplePosition3(PeoplePositionN):
    class Meta:
        db_table = "peopleposition3"


class PeoplePosition4(PeoplePositionN):
    class Meta:
        db_table = "peopleposition4"


class PeoplePosition5(PeoplePositionN):
    class Meta:
        db_table = "peopleposition5"


class PeoplePosition6(PeoplePositionN):
    class Meta:
        db_table = "peopleposition6"


class PeoplePosition7(PeoplePositionN):
    class Meta:
        db_table = "peopleposition7"


class PeoplePosition8(PeoplePositionN):
    class Meta:
        db_table = "peopleposition9"
