from django.db import models


# Create your models here.

class MobileBrand(models.Model):
    id = models.SmallIntegerField(db_column="id", verbose_name="品牌标识主键",primary_key=True,unique=True)
    name = models.CharField(max_length=32, db_column="name", verbose_name="品牌名")
    # ddate = models.DateField(db_column="ddate", verbose_name="日期")
    # rate = models.FloatField(db_column="rate", verbose_name="品牌占有率")

    class Meta:
        db_table = "mobilebrand"


# class MobileModel(models.Model):
#     pid = models.ForeignKey(to="MobileBrand", to_field="pid", on_delete=models.CASCADE, db_column="pid",
#                             verbose_name="品牌标识外键")
#     mpid = models.SmallIntegerField(db_column="mpid", verbose_name="机型标识", unique=True, db_index=True)
#     mmodel = models.CharField(max_length=32, db_column="mmodel", verbose_name="机型")
#     ddate = models.DateField(db_column="ddate", verbose_name="日期")
#     rate = models.FloatField(db_column="rate", verbose_name="机型占有率")
#     brandtype = models.CharField(max_length=8, db_column="brandtype", verbose_name="品牌分类:安卓，苹果")
#
#     class Meta:
#         db_table = "mobilemodel"


class ModelModel(models.Model):
    pid = models.SmallIntegerField(db_column="pid", verbose_name="标识")
    version = models.CharField(db_column="version", max_length=32, verbose_name="类型名")
    ddate = models.DateField(db_column="ddate", verbose_name="日期")
    rate = models.FloatField(db_column="rate", verbose_name="占有率")

    class Meta:
        abstract = True


class Mobileystem(ModelModel):
    class Meta:
        db_table = "mobilesystem"


class Operator(ModelModel):
    class Meta:
        db_table = "operator"


class NetWork(ModelModel):
    class Meta:
        db_table = "network"


class UserHabit(models.Model):
    ddate = models.DateField(db_column="ddate")
    installnum = models.SmallIntegerField(db_column="installnum")
    activenum = models.SmallIntegerField(db_column="activenum")

    class Meta:
        db_table = "userhabit"
