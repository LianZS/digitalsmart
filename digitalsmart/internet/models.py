from django.db import models


# Create your models here.

class MobileBrand(models.Model):
    # 品牌概况表
    id = models.SmallIntegerField(db_column="id", verbose_name="品牌标识主键", primary_key=True)
    name = models.CharField(max_length=32, db_column="name", verbose_name="品牌名")

    class Meta:
        db_table = "mobilebrand"


class MobileModel(models.Model):
    # 品牌手机机型占有率
    pid = models.ForeignKey(to="MobileBrand", to_field="id", on_delete=models.CASCADE, db_column="pid",
                            verbose_name="品牌标识外键")
    mpid = models.SmallIntegerField(db_column="mpid", verbose_name="机型标识")
    mmodel = models.CharField(max_length=32, db_column="mmodel", verbose_name="机型")
    ddate = models.DateField(db_column="ddate", verbose_name="日期")
    rate = models.FloatField(db_column="rate", verbose_name="机型占有率")
    brandtype = models.CharField(max_length=8, db_column="brandtype", verbose_name="品牌分类:安卓，苹果")

    class Meta:
        db_table = "mobilemodel"
        index_together=[["mpid","pid"]]


class BrandShare(models.Model):
    pid = models.ForeignKey(to="MobileBrand", to_field="id", on_delete=models.CASCADE, db_column="pid", db_index=True,
                            verbose_name="品牌标识外键")
    ddate = models.DateField(db_column="ddate", verbose_name="日期")
    rate = models.FloatField(db_column="rate", verbose_name="品牌占有率")
    class Meta:
        db_table="brandshare"




class Operator(models.Model):
    # 运营商总览表
    id = models.SmallIntegerField(db_column="id", primary_key=True, verbose_name="标识")
    name = models.CharField(max_length=18, db_column="name", verbose_name="运营商名")

    class Meta:
        db_table = "operator"


class OperatorRate(models.Model):
    # 运营商占有率表
    pid = models.ForeignKey(to="Operator", to_field="id", db_column="pid", db_index=True, verbose_name="标识",
                            on_delete=models.CASCADE)
    ddate = models.DateField(db_column="ddate", verbose_name="日期")
    rate = models.FloatField(db_column="rate", verbose_name="运营商占有率")

    class Meta:
        db_table = "operatorrate"


class MobileSystemVersion(models.Model):
    #
    id = models.SmallIntegerField(db_column="id", primary_key=True, verbose_name="系统版本标识id")
    version = models.CharField(max_length=18, db_column="version", verbose_name="系统版本")
    category = models.CharField(max_length=5, db_column="category", verbose_name="系统归属（苹果，安卓）")

    class Meta:
        db_table = "mobilesystemversion"


class MobileSystemRate(models.Model):
    pid = models.ForeignKey(to="MobileSystemVersion", to_field="id", db_column="pid", verbose_name="系统版本标识",
                            on_delete=models.CASCADE, db_index=True, )
    ddate = models.DateField(db_column="ddate", verbose_name="日期")
    rate = models.FloatField(db_column="rate", verbose_name="手机系统占有率")

    class Meta:
        db_table = "mobilesystemrate"


class Network(models.Model):
    id = models.SmallIntegerField(db_column="id", primary_key=True, verbose_name="网络标识")
    name = models.CharField(max_length=4, db_column="name", verbose_name="网络名（3G,4G.5G,WIFI..）")

    class Meta:
        db_table = "network"


class NetworkShare(models.Model):
    pid = models.ForeignKey(to="Network", to_field="id", db_column="pid", verbose_name="网络标识", db_index=True,
                            on_delete=models.CASCADE)

    ddate = models.DateField(db_column="ddate", verbose_name="日期")
    rate = models.FloatField(db_column="rate", verbose_name="网络占有率")

    class Meta:
        db_table = "networkshare"


class UserHabit(models.Model):
    ddate = models.DateField(db_column="ddate", verbose_name="日期")
    installnum = models.SmallIntegerField(db_column="installnum", verbose_name="人均安装应用")
    activenum = models.SmallIntegerField(db_column="activenum", verbose_name="人均安装应用")

    class Meta:
        db_table = "userhabit"


class AppInfo(models.Model):
    id = models.IntegerField(db_column="id",primary_key=True)
    appname = models.CharField(max_length=32, db_column="name", verbose_name="app名字")
    boy = models.FloatField(db_column="boy", verbose_name="男生占有率")
    girl = models.FloatField(db_column="girl", verbose_name="女生占有率")

    class Meta:
        db_table = "appinfo"


class AppActive(models.Model):
    #创建无效果
    pid = models.ForeignKey(to="AppInfo", to_field="id", db_column="pid", verbose_name="app标识", db_index=True,
                            on_delete=models.CASCADE)
    ddate = models.DateField(db_column="ddate", verbose_name="日期")
    activenum = models.IntegerField(db_column="activenum", verbose_name="活跃数")
    activerate = models.FloatField(db_column="activerate", verbose_name="活跃度")

    base_activerate = models.FloatField(db_column="base_activerate", verbose_name="行业活跃度基准值")

    aver_activerate = models.FloatField(db_column="aver_activerate", verbose_name="行业活跃度均值")

    class Meta:
        db_table = "appactive"


class AgeShare(models.Model):
    pid = models.ForeignKey(to="AppInfo", to_field="id", db_column="pid", verbose_name="app标识", db_index=True,
                            on_delete=models.CASCADE)
    under_nineth = models.FloatField(db_column="under_nineth", verbose_name="19岁以下占比")
    nin_twen = models.FloatField(db_column="nin_twen", verbose_name="19-25岁占比")
    twe_thir = models.FloatField(db_column="twe_thir", verbose_name="26-35岁占比")

    thir_four = models.FloatField(db_column="thir_four", verbose_name="36-45岁占比")

    four_fift = models.FloatField(db_column="four_fift", verbose_name="46-55岁占比")
    over_fift = models.FloatField(db_column="over_fift", verbose_name="55岁以上占比")

    class Meta:
        db_table = "ageshare"

class AppLike(models.Model):
    pid = models.ForeignKey(to="AppInfo", to_field="id", db_column="pid", verbose_name="app标识", db_index=True,
                            on_delete=models.CASCADE)
    keyword =models.CharField(max_length=32,verbose_name="keyword")
    rate = models.FloatField(db_column="rate", verbose_name="应用偏好占有率")
    class Meta:
        db_table="applike"

class AppProvinceShare(models.Model):
    pid = models.ForeignKey(to="AppInfo", to_field="id", db_column="pid", verbose_name="app标识", db_index=True,
                            on_delete=models.CASCADE)
    province =models.CharField(max_length=16,verbose_name="province")
    rate = models.FloatField(db_column="rate", verbose_name="省份占有率")
    class Meta:
        db_table="app_province_share"
