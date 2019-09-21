from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ScenceManager(models.Model):
    """
    信息概况总表
    """
    pid = models.SmallIntegerField(db_column="pid", verbose_name="标识")
    area = models.CharField(db_column="area", max_length=32, verbose_name="地名")
    longitude = models.FloatField(db_column="longitude", verbose_name="中心经度")
    latitude = models.FloatField(db_column="latitude", verbose_name="中心纬度")
    loaction = models.CharField(db_column="loaction", max_length=18, verbose_name="所处城市")
    citypid = models.IntegerField(db_column="citypid", verbose_name="所处城市标识")
    weatherpid = models.TextField(db_column="weatherpid", verbose_name="对应的天气标识")
    flag = models.SmallIntegerField(db_column="flag", verbose_name="是否公开，0表示公开")
    province = models.CharField(db_column="province", max_length=18, verbose_name="省份")
    type_flag = models.SmallIntegerField(db_column="type_flag", verbose_name="类别标识,百度数据为1，腾讯为0")

    class Meta:
        db_table = "scencemanager"


class SearchRate(models.Model):
    """
    地名搜索频率
    """
    pid = models.SmallIntegerField(db_index=True, db_column="pid", verbose_name="标识")
    tmp_date = models.IntegerField(db_column="tmp_date", verbose_name="时间,格式为yyyymmdd")
    area = models.CharField(db_column="area", max_length=32, verbose_name="地名")
    rate = models.IntegerField(db_column="rate", verbose_name="频率")
    name = models.CharField(max_length=16, db_column="name", verbose_name="搜索引擎，包括微信-wechat，百度-baidu，搜狗-sougou")
    flag = models.SmallIntegerField(db_column="flag", verbose_name="是否公开", default=0)

    class Meta:
        db_table = "searchrate"


class Geographic(models.Model):
    """
    地区范围经纬度

    """
    pid = models.SmallIntegerField(db_index=True, db_column="pid", verbose_name="标识")
    longitude = models.FloatField(db_column="longitude", verbose_name="经度")
    latitude = models.CharField(max_length=18, db_column="latitude", verbose_name="维度")
    flag = models.SmallIntegerField(verbose_name="类别标识flag(百度数据为1，腾讯为0", db_column="flag")

    class Meta:
        db_table = "geographic"


class ScenceTrend(models.Model):
    """
    地区人口趋势

    """
    pid = models.SmallIntegerField(db_column="pid", verbose_name="标识")
    ddate = models.IntegerField(db_column="ddate", verbose_name="日期,格式为yyyymmdd")
    ttime = models.TimeField(db_column="ttime", verbose_name="时间,格式为HH：MM：SS")
    rate = models.FloatField(db_column="rate", verbose_name="频率")

    class Meta:
        db_table = "scencetrend"
        index_together = ['pid', 'ddate', 'ttime', 'rate']


class TableManager(models.Model):
    pid = models.SmallIntegerField(verbose_name="标识")
    area = models.CharField(max_length=32, verbose_name="地名")
    last_date = models.IntegerField(verbose_name="最近更新时间--时间戳，根据时间戳查找数据")
    table_id = models.SmallIntegerField(verbose_name="对应表格标识，表格标识为0-9")
    flag = models.SmallIntegerField(verbose_name="类别标识flag(百度数据为1，腾讯为0", db_column="flag")

    class Meta:
        db_table = "tablemanager"


class UserProfile(models.Model):  # 存放用户信息
    user = models.OneToOneField(User, unique=True, verbose_name="用户", on_delete=models.CASCADE)
    idcard = models.BigIntegerField(db_column="idcard", verbose_name="身份证", null=False)
    photo = models.ImageField(upload_to="user", null=True)  # 头像

    class Meta:
        db_table = "userdb"


class ScenceImage(models.Model):
    # 景区图片
    pid = models.SmallIntegerField(db_column="pid", verbose_name="标识")
    photo = models.ImageField(upload_to="photo")

    class Meta:
        db_table = "photodb"


class CommentRate(models.Model):
    # 景区评价关键词指数
    pid = models.IntegerField(db_column="pid")

    adjectives = models.CharField(max_length=16, db_column="adjectives", verbose_name="形容词")
    rate = models.FloatField(db_column="rate", verbose_name="评分")

    # num = models.SmallIntegerField(db_column="num",verbose_name="第几条")
    class Meta:
        db_table = "comment_rate"


class NetComment(models.Model):
    # 网友评论
    pid = models.IntegerField(db_column="pid", db_index=True)
    commentuser = models.CharField(max_length=32, db_column="commentuser", verbose_name="网友")
    comment = models.TextField(db_column="comment", verbose_name="评论")
    commenttime = models.DateField(db_column="commenttime", verbose_name="评论时间")
    commentlike = models.SmallIntegerField(db_column="commentlike", verbose_name="星级好感数（1-5）")
    userphoto = models.ImageField(upload_to="user", db_column="userphoto", verbose_name="网友头像")

    class Meta:
        db_table = "comment"


class ScenceState(models.Model):
    """景区总状况"""
    pid = models.IntegerField(db_column="pid")
    trafficstate = models.CharField(max_length=16, db_column="trafficstate", verbose_name="交通状况")
    weatherstate = models.CharField(max_length=16, db_column="weatherstate", verbose_name="天气状况")
    coststate = models.CharField(max_length=16, db_column="coststate", verbose_name="性价比状况")
    environmentstate = models.CharField(max_length=16, db_column="environmentstate", verbose_name="环境状况")

    class Meta:
        db_table = "scencestate"


class PredictParamer(models.Model):
    """
    景区预测模型
    """
    pid = models.IntegerField(db_column="pid", verbose_name="景区标识")
    flag = models.BooleanField(db_column="flag", verbose_name="是否为重大节假日，是的话为1")
    hconstant = models.FloatField(db_column="hconstant", verbose_name="最高项系数")
    hpower = models.SmallIntegerField(db_column="hpower", verbose_name="最高次幂")
    sconstant = models.FloatField(db_column="sconstant", verbose_name="二次项系数")
    spower = models.SmallIntegerField(db_column="spower", verbose_name="二次次幂")
    lconstant = models.FloatField(db_column="lconstant", verbose_name="一次项系数")
    lpower = models.SmallIntegerField(db_column="lpower", verbose_name="一次次幂")
    mconstant = models.FloatField(db_column="mconstant", verbose_name=" 常数项")

    class Meta:
        db_table = "predictmodel"


class Historyscenceflow(models.Model):
    """
    地区实时客流量数据模板
    """
    pid = models.SmallIntegerField(db_column="pid", verbose_name="景区标识")
    ddate = models.IntegerField(db_column="ddate", verbose_name="日期,格式为yyyymmdd")
    ttime = models.TimeField(db_column="ttime", verbose_name="时间,格式为HH：MM：SS")
    num = models.IntegerField(db_column="num", verbose_name="总人数")

    def __str__(self):
        return "标识：{0}，日期：{1}，时间：{2}，数量：{3}".format(self.pid, self.ddate, self.ttime, self.num)

    class Meta:
        abstract = True
        index_together = ['ddate', 'ttime', 'num']


class Historyscenceflow1(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow1'


class Historyscenceflow2(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow2'


class Historyscenceflow3(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow3'


class Historyscenceflow4(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow4'


class Historyscenceflow5(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow5'


class Historyscenceflow6(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow6'


class Historyscenceflow7(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow7'


class Historyscenceflow8(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow8'


class Historyscenceflow9(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow9'


class Historyscenceflow10(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow10'


class Historyscenceflow11(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow11'


class Historyscenceflow12(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow12'


class Historyscenceflow13(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow13'


class Historyscenceflow14(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow14'


class Historyscenceflow15(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow15'


class Historyscenceflow16(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow16'


class Historyscenceflow17(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow17'


class Historyscenceflow18(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow18'


class Historyscenceflow19(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow19'


class Historyscenceflow20(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow20'


class Historyscenceflow21(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow21'


class Historyscenceflow22(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow22'


class Historyscenceflow23(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow23'


class Historyscenceflow24(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow24'


class Historyscenceflow25(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow25'


class Historyscenceflow26(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow26'


class Historyscenceflow27(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow27'


class Historyscenceflow28(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow28'


class Historyscenceflow29(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow29'


class Historyscenceflow30(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow30'


class Historyscenceflow31(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow31'


class Historyscenceflow32(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow32'


class Historyscenceflow33(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow33'


class Historyscenceflow34(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow34'


class Historyscenceflow35(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow35'


class Historyscenceflow36(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow36'


class Historyscenceflow37(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow37'


class Historyscenceflow38(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow38'


class Historyscenceflow39(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow39'


class Historyscenceflow40(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow40'


class Historyscenceflow41(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow41'


class Historyscenceflow42(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow42'


class Historyscenceflow43(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow43'


class Historyscenceflow44(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow44'


class Historyscenceflow45(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow45'


class Historyscenceflow46(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow46'


class Historyscenceflow47(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow47'


class Historyscenceflow48(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow48'


class Historyscenceflow49(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow49'


class Historyscenceflow50(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow50'


class Historyscenceflow51(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow51'


class Historyscenceflow52(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow52'


class Historyscenceflow53(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow53'


class Historyscenceflow54(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow54'


class Historyscenceflow55(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow55'


class Historyscenceflow56(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow56'


class Historyscenceflow57(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow57'


class Historyscenceflow58(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow58'


class Historyscenceflow59(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow59'


class Historyscenceflow60(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow60'


class Historyscenceflow61(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow61'


class Historyscenceflow62(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow62'


class Historyscenceflow63(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow63'


class Historyscenceflow64(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow64'


class Historyscenceflow65(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow65'


class Historyscenceflow66(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow66'


class Historyscenceflow67(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow67'


class Historyscenceflow68(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow68'


class Historyscenceflow69(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow69'


class Historyscenceflow70(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow70'


class Historyscenceflow71(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow71'


class Historyscenceflow72(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow72'


class Historyscenceflow73(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow73'


class Historyscenceflow74(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow74'


class Historyscenceflow75(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow75'


class Historyscenceflow76(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow76'


class Historyscenceflow77(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow77'


class Historyscenceflow78(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow78'


class Historyscenceflow79(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow79'


class Historyscenceflow80(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow80'


class Historyscenceflow81(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow81'


class Historyscenceflow82(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow82'


class Historyscenceflow83(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow83'


class Historyscenceflow84(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow84'


class Historyscenceflow85(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow85'


class Historyscenceflow86(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow86'


class Historyscenceflow87(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow87'


class Historyscenceflow88(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow88'


class Historyscenceflow89(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow89'


class Historyscenceflow90(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow90'


class Historyscenceflow91(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow91'


class Historyscenceflow92(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow92'


class Historyscenceflow93(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow93'


class Historyscenceflow94(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow94'


class Historyscenceflow95(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow95'


class Historyscenceflow96(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow96'


class Historyscenceflow97(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow97'


class Historyscenceflow98(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow98'


class Historyscenceflow99(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow99'


class Historyscenceflow100(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow100'


class Historyscenceflow101(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow101'


class Historyscenceflow102(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow102'


class Historyscenceflow103(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow103'


class Historyscenceflow104(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow104'


class Historyscenceflow105(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow105'


class Historyscenceflow106(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow106'


class Historyscenceflow107(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow107'


class Historyscenceflow108(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow108'


class Historyscenceflow109(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow109'


class Historyscenceflow110(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow110'


class Historyscenceflow111(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow111'


class Historyscenceflow112(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow112'


class Historyscenceflow113(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow113'


class Historyscenceflow114(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow114'


class Historyscenceflow115(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow115'


class Historyscenceflow116(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow116'


class Historyscenceflow117(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow117'


class Historyscenceflow118(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow118'


class Historyscenceflow119(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow119'


class Historyscenceflow120(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow120'


class Historyscenceflow121(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow121'


class Historyscenceflow122(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow122'


class Historyscenceflow123(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow123'


class Historyscenceflow124(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow124'


class Historyscenceflow125(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow125'


class Historyscenceflow126(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow126'


class Historyscenceflow127(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow127'


class Historyscenceflow128(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow128'


class Historyscenceflow129(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow129'


class Historyscenceflow130(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow130'


class Historyscenceflow131(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow131'


class Historyscenceflow132(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow132'


class Historyscenceflow133(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow133'


class Historyscenceflow134(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow134'


class Historyscenceflow135(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow135'


class Historyscenceflow136(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow136'


class Historyscenceflow137(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow137'


class Historyscenceflow138(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow138'


class Historyscenceflow139(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow139'


class Historyscenceflow140(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow140'


class Historyscenceflow141(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow141'


class Historyscenceflow142(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow142'


class Historyscenceflow143(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow143'


class Historyscenceflow144(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow144'


class Historyscenceflow145(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow145'


class Historyscenceflow146(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow146'


class Historyscenceflow147(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow147'


class Historyscenceflow148(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow148'


class Historyscenceflow149(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow149'


class Historyscenceflow150(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow150'


class Historyscenceflow151(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow151'


class Historyscenceflow152(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow152'


class Historyscenceflow153(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow153'


class Historyscenceflow154(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow154'


class Historyscenceflow155(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow155'


class Historyscenceflow156(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow156'


class Historyscenceflow157(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow157'


class Historyscenceflow158(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow158'


class Historyscenceflow159(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow159'


class Historyscenceflow160(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow160'


class Historyscenceflow161(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow161'


class Historyscenceflow162(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow162'


class Historyscenceflow163(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow163'


class Historyscenceflow164(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow164'


class Historyscenceflow165(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow165'


class Historyscenceflow166(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow166'


class Historyscenceflow167(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow167'


class Historyscenceflow168(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow168'


class Historyscenceflow169(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow169'


class Historyscenceflow170(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow170'


class Historyscenceflow171(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow171'


class Historyscenceflow172(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow172'


class Historyscenceflow173(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow173'


class Historyscenceflow174(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow174'


class Historyscenceflow175(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow175'


class Historyscenceflow176(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow176'


class Historyscenceflow177(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow177'


class Historyscenceflow178(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow178'


class Historyscenceflow179(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow179'


class Historyscenceflow180(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow180'


class Historyscenceflow181(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow181'


class Historyscenceflow182(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow182'


class Historyscenceflow183(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow183'


class Historyscenceflow184(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow184'


class Historyscenceflow185(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow185'


class Historyscenceflow186(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow186'


class Historyscenceflow187(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow187'


class Historyscenceflow188(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow188'


class Historyscenceflow189(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow189'


class Historyscenceflow190(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow190'


class Historyscenceflow191(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow191'


class Historyscenceflow192(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow192'


class Historyscenceflow193(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow193'


class Historyscenceflow194(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow194'


class Historyscenceflow195(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow195'


class Historyscenceflow196(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow196'


class Historyscenceflow197(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow197'


class Historyscenceflow198(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow198'


class Historyscenceflow199(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow199'


class Historyscenceflow200(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow200'


class Historyscenceflow201(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow201'


class Historyscenceflow202(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow202'


class Historyscenceflow203(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow203'


class Historyscenceflow204(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow204'


class Historyscenceflow205(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow205'


class Historyscenceflow206(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow206'


class Historyscenceflow207(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow207'


class Historyscenceflow208(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow208'


class Historyscenceflow209(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow209'


class Historyscenceflow210(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow210'


class Historyscenceflow211(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow211'


class Historyscenceflow212(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow212'


class Historyscenceflow213(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow213'


class Historyscenceflow214(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow214'


class Historyscenceflow215(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow215'


class Historyscenceflow216(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow216'


class Historyscenceflow217(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow217'


class Historyscenceflow218(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow218'


class Historyscenceflow219(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow219'


class Historyscenceflow220(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow220'


class Historyscenceflow221(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow221'


class Historyscenceflow222(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow222'


class Historyscenceflow223(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow223'


class Historyscenceflow224(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow224'


class Historyscenceflow225(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow225'


class Historyscenceflow226(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow226'


class Historyscenceflow227(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow227'


class Historyscenceflow228(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow228'


class Historyscenceflow229(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow229'


class Historyscenceflow230(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow230'


class Historyscenceflow231(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow231'


class Historyscenceflow232(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow232'


class Historyscenceflow233(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow233'


class Historyscenceflow234(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow234'


class Historyscenceflow235(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow235'


class Historyscenceflow236(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow236'


class Historyscenceflow237(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow237'


class Historyscenceflow238(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow238'


class Historyscenceflow239(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow239'


class Historyscenceflow240(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow240'


class Historyscenceflow241(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow241'


class Historyscenceflow242(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow242'


class Historyscenceflow243(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow243'


class Historyscenceflow244(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow244'


class Historyscenceflow245(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow245'


class Historyscenceflow246(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow246'


class Historyscenceflow247(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow247'


class Historyscenceflow248(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow248'


class Historyscenceflow249(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow249'


class Historyscenceflow250(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow250'


class Historyscenceflow251(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow251'


class Historyscenceflow252(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow252'


class Historyscenceflow253(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow253'


class Historyscenceflow254(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow254'


class Historyscenceflow255(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow255'


class Historyscenceflow256(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow256'


class Historyscenceflow257(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow257'


class Historyscenceflow258(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow258'


class Historyscenceflow259(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow259'


class Historyscenceflow260(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow260'


class Historyscenceflow261(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow261'


class Historyscenceflow262(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow262'


class Historyscenceflow263(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow263'


class Historyscenceflow264(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow264'


class Historyscenceflow265(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow265'


class Historyscenceflow266(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow266'


class Historyscenceflow267(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow267'


class Historyscenceflow268(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow268'


class Historyscenceflow269(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow269'


class Historyscenceflow270(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow270'


class Historyscenceflow271(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow271'


class Historyscenceflow272(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow272'


class Historyscenceflow273(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow273'


class Historyscenceflow274(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow274'


class Historyscenceflow275(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow275'


class Historyscenceflow276(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow276'


class Historyscenceflow277(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow277'


class Historyscenceflow278(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow278'


class Historyscenceflow279(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow279'


class Historyscenceflow280(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow280'


class Historyscenceflow281(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow281'


class Historyscenceflow282(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow282'


class Historyscenceflow283(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow283'


class Historyscenceflow284(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow284'


class Historyscenceflow285(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow285'


class Historyscenceflow286(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow286'


class Historyscenceflow287(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow287'


class Historyscenceflow288(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow288'


class Historyscenceflow289(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow289'


class Historyscenceflow290(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow290'


class Historyscenceflow291(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow291'


class Historyscenceflow292(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow292'


class Historyscenceflow293(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow293'


class Historyscenceflow294(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow294'


class Historyscenceflow295(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow295'


class Historyscenceflow296(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow296'


class Historyscenceflow297(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow297'


class Historyscenceflow298(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow298'


class Historyscenceflow299(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow299'


class Historyscenceflow300(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow300'


class Historyscenceflow301(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow301'


class Historyscenceflow302(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow302'


class Historyscenceflow303(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow303'


class Historyscenceflow304(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow304'


class Historyscenceflow305(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow305'


class Historyscenceflow306(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow306'


class Historyscenceflow307(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow307'


class Historyscenceflow308(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow308'


class Historyscenceflow309(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow309'


class Historyscenceflow310(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow310'


class Historyscenceflow311(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow311'


class Historyscenceflow312(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow312'


class Historyscenceflow313(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow313'


class Historyscenceflow314(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow314'


class Historyscenceflow315(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow315'


class Historyscenceflow316(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow316'


class Historyscenceflow317(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow317'


class Historyscenceflow318(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow318'


class Historyscenceflow319(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow319'


class Historyscenceflow320(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow320'


class Historyscenceflow321(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow321'


class Historyscenceflow322(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow322'


class Historyscenceflow323(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow323'


class Historyscenceflow324(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow324'


class Historyscenceflow325(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow325'


class Historyscenceflow326(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow326'


class Historyscenceflow327(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow327'


class Historyscenceflow328(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow328'


class Historyscenceflow329(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow329'


class Historyscenceflow330(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow330'


class Historyscenceflow331(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow331'


class Historyscenceflow332(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow332'


class Historyscenceflow333(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow333'


class Historyscenceflow334(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow334'


class Historyscenceflow335(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow335'


class Historyscenceflow336(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow336'


class Historyscenceflow337(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow337'


class Historyscenceflow338(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow338'


class Historyscenceflow339(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow339'


class Historyscenceflow340(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow340'


class Historyscenceflow341(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow341'


class Historyscenceflow342(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow342'


class Historyscenceflow343(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow343'


class Historyscenceflow344(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow344'


class Historyscenceflow345(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow345'


class Historyscenceflow346(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow346'


class Historyscenceflow347(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow347'


class Historyscenceflow348(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow348'


class Historyscenceflow349(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow349'


class Historyscenceflow350(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow350'


class Historyscenceflow351(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow351'


class Historyscenceflow352(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow352'


class Historyscenceflow353(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow353'


class Historyscenceflow354(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow354'


class Historyscenceflow355(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow355'


class Historyscenceflow356(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow356'


class Historyscenceflow357(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow357'


class Historyscenceflow358(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow358'


class Historyscenceflow359(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow359'


class Historyscenceflow360(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow360'


class Historyscenceflow361(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow361'


class Historyscenceflow362(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow362'


class Historyscenceflow363(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow363'


class Historyscenceflow364(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow364'


class Historyscenceflow365(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow365'


class Historyscenceflow366(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow366'


class Historyscenceflow367(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow367'


class Historyscenceflow368(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow368'


class Historyscenceflow369(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow369'


class Historyscenceflow370(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow370'


class Historyscenceflow371(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow371'


class Historyscenceflow372(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow372'


class Historyscenceflow373(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow373'


class Historyscenceflow374(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow374'


class Historyscenceflow375(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow375'


class Historyscenceflow376(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow376'


class Historyscenceflow377(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow377'


class Historyscenceflow378(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow378'


class Historyscenceflow379(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow379'


class Historyscenceflow380(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow380'


class Historyscenceflow381(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow381'


class Historyscenceflow382(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow382'


class Historyscenceflow383(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow383'


class Historyscenceflow384(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow384'


class Historyscenceflow385(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow385'


class Historyscenceflow386(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow386'


class Historyscenceflow387(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow387'


class Historyscenceflow388(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow388'


class Historyscenceflow389(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow389'


class Historyscenceflow390(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow390'


class Historyscenceflow391(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow391'


class Historyscenceflow392(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow392'


class Historyscenceflow393(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow393'


class Historyscenceflow394(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow394'


class Historyscenceflow395(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow395'


class Historyscenceflow396(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow396'


class Historyscenceflow397(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow397'


class Historyscenceflow398(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow398'


class Historyscenceflow399(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow399'


class Historyscenceflow400(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow400'


class Historyscenceflow401(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow401'


class Historyscenceflow402(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow402'


class Historyscenceflow403(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow403'


class Historyscenceflow404(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow404'


class Historyscenceflow405(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow405'


class Historyscenceflow406(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow406'


class Historyscenceflow407(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow407'


class Historyscenceflow408(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow408'


class Historyscenceflow409(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow409'


class Historyscenceflow410(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow410'


class Historyscenceflow411(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow411'


class Historyscenceflow412(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow412'


class Historyscenceflow413(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow413'


class Historyscenceflow414(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow414'


class Historyscenceflow415(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow415'


class Historyscenceflow416(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow416'


class Historyscenceflow417(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow417'


class Historyscenceflow418(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow418'


class Historyscenceflow419(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow419'


class Historyscenceflow420(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow420'


class Historyscenceflow421(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow421'


class Historyscenceflow422(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow422'


class Historyscenceflow423(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow423'


class Historyscenceflow424(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow424'


class Historyscenceflow425(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow425'


class Historyscenceflow426(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow426'


class Historyscenceflow427(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow427'


class Historyscenceflow428(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow428'


class Historyscenceflow429(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow429'


class Historyscenceflow430(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow430'


class Historyscenceflow431(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow431'


class Historyscenceflow432(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow432'


class Historyscenceflow433(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow433'


class Historyscenceflow434(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow434'


class Historyscenceflow435(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow435'


class Historyscenceflow436(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow436'


class Historyscenceflow437(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow437'


class Historyscenceflow438(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow438'


class Historyscenceflow439(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow439'


class Historyscenceflow440(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow440'


class Historyscenceflow441(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow441'


class Historyscenceflow442(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow442'


class Historyscenceflow443(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow443'


class Historyscenceflow444(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow444'


class Historyscenceflow445(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow445'


class Historyscenceflow446(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow446'


class Historyscenceflow447(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow447'


class Historyscenceflow448(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow448'


class Historyscenceflow449(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow449'


class Historyscenceflow450(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow450'


class Historyscenceflow451(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow451'


class Historyscenceflow452(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow452'


class Historyscenceflow453(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow453'


class Historyscenceflow454(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow454'


class Historyscenceflow455(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow455'


class Historyscenceflow456(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow456'


class Historyscenceflow457(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow457'


class Historyscenceflow458(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow458'


class Historyscenceflow459(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow459'


class Historyscenceflow460(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow460'


class Historyscenceflow461(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow461'


class Historyscenceflow462(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow462'


class Historyscenceflow463(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow463'


class Historyscenceflow464(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow464'


class Historyscenceflow465(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow465'


class Historyscenceflow466(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow466'


class Historyscenceflow467(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow467'


class Historyscenceflow468(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow468'


class Historyscenceflow469(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow469'


class Historyscenceflow470(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow470'


class Historyscenceflow471(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow471'


class Historyscenceflow472(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow472'


class Historyscenceflow473(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow473'


class Historyscenceflow474(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow474'


class Historyscenceflow475(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow475'


class Historyscenceflow476(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow476'


class Historyscenceflow477(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow477'


class Historyscenceflow478(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow478'


class Historyscenceflow479(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow479'


class Historyscenceflow480(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow480'


class Historyscenceflow481(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow481'


class Historyscenceflow482(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow482'


class Historyscenceflow483(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow483'


class Historyscenceflow484(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow484'


class Historyscenceflow485(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow485'


class Historyscenceflow486(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow486'


class Historyscenceflow487(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow487'


class Historyscenceflow488(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow488'


class Historyscenceflow489(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow489'


class Historyscenceflow490(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow490'


class Historyscenceflow491(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow491'


class Historyscenceflow492(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow492'


class Historyscenceflow493(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow493'


class Historyscenceflow494(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow494'


class Historyscenceflow495(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow495'


class Historyscenceflow496(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow496'


class Historyscenceflow497(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow497'


class Historyscenceflow498(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow498'


class Historyscenceflow499(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow499'


class Historyscenceflow500(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow500'


class Historyscenceflow501(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow501'


class Historyscenceflow502(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow502'


class Historyscenceflow503(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow503'


class Historyscenceflow504(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow504'


class Historyscenceflow505(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow505'


class Historyscenceflow506(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow506'


class Historyscenceflow507(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow507'


class Historyscenceflow508(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow508'


class Historyscenceflow509(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow509'


class Historyscenceflow510(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow510'


class Historyscenceflow511(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow511'


class Historyscenceflow512(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow512'


class Historyscenceflow513(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow513'


class Historyscenceflow514(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow514'


class Historyscenceflow515(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow515'


class Historyscenceflow516(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow516'


class Historyscenceflow517(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow517'


class Historyscenceflow518(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow518'


class Historyscenceflow519(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow519'


class Historyscenceflow520(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow520'


class Historyscenceflow521(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow521'


class Historyscenceflow522(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow522'


class Historyscenceflow523(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow523'


class Historyscenceflow524(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow524'


class Historyscenceflow525(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow525'


class Historyscenceflow526(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow526'


class Historyscenceflow527(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow527'


class Historyscenceflow528(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow528'


class Historyscenceflow529(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow529'


class Historyscenceflow530(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow530'


class Historyscenceflow531(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow531'


class Historyscenceflow532(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow532'


class Historyscenceflow533(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow533'


class Historyscenceflow534(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow534'


class Historyscenceflow535(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow535'


class Historyscenceflow536(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow536'


class Historyscenceflow537(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow537'


class Historyscenceflow538(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow538'


class Historyscenceflow539(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow539'


class Historyscenceflow540(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow540'


class Historyscenceflow541(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow541'


class Historyscenceflow542(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow542'


class Historyscenceflow543(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow543'


class Historyscenceflow544(Historyscenceflow):
    class Meta:
        db_table = 'historyscenceflow544'


class PeoplePosition(models.Model):
    """
    人口分布分表父类

    """
    pid = models.SmallIntegerField(db_column="pid", verbose_name="标识")
    area = models.CharField(max_length=32, db_column="area", verbose_name="地名")
    lon = models.FloatField(verbose_name="经度", db_column="lon")
    lat = models.FloatField(verbose_name="纬度", db_column="lat")
    num = models.SmallIntegerField(verbose_name="人数", db_column="num")

    class Meta:
        abstract = True
        index_together = ['tmp_date']


class PeoplePosition1(PeoplePosition):
    class Meta:
        db_table = 'peopleposition1'


class PeoplePosition2(PeoplePosition):
    class Meta:
        db_table = 'peopleposition2'


class PeoplePosition3(PeoplePosition):
    class Meta:
        db_table = 'peopleposition3'


class PeoplePosition4(PeoplePosition):
    class Meta:
        db_table = 'peopleposition4'


class PeoplePosition5(PeoplePosition):
    class Meta:
        db_table = 'peopleposition5'


class PeoplePosition6(PeoplePosition):
    class Meta:
        db_table = 'peopleposition6'


class PeoplePosition7(PeoplePosition):
    class Meta:
        db_table = 'peopleposition7'


class PeoplePosition8(PeoplePosition):
    class Meta:
        db_table = 'peopleposition8'


class PeoplePosition9(PeoplePosition):
    class Meta:
        db_table = 'peopleposition9'


class PeoplePosition10(PeoplePosition):
    class Meta:
        db_table = 'peopleposition10'


class PeoplePosition11(PeoplePosition):
    class Meta:
        db_table = 'peopleposition11'


class PeoplePosition12(PeoplePosition):
    class Meta:
        db_table = 'peopleposition12'


class PeoplePosition13(PeoplePosition):
    class Meta:
        db_table = 'peopleposition13'


class PeoplePosition14(PeoplePosition):
    class Meta:
        db_table = 'peopleposition14'


class PeoplePosition15(PeoplePosition):
    class Meta:
        db_table = 'peopleposition15'


class PeoplePosition16(PeoplePosition):
    class Meta:
        db_table = 'peopleposition16'


class PeoplePosition17(PeoplePosition):
    class Meta:
        db_table = 'peopleposition17'


class PeoplePosition18(PeoplePosition):
    class Meta:
        db_table = 'peopleposition18'


class PeoplePosition19(PeoplePosition):
    class Meta:
        db_table = 'peopleposition19'


class PeoplePosition20(PeoplePosition):
    class Meta:
        db_table = 'peopleposition20'


class PeoplePosition21(PeoplePosition):
    class Meta:
        db_table = 'peopleposition21'


class PeoplePosition22(PeoplePosition):
    class Meta:
        db_table = 'peopleposition22'


class PeoplePosition23(PeoplePosition):
    class Meta:
        db_table = 'peopleposition23'


class PeoplePosition24(PeoplePosition):
    class Meta:
        db_table = 'peopleposition24'


class PeoplePosition25(PeoplePosition):
    class Meta:
        db_table = 'peopleposition25'


class PeoplePosition26(PeoplePosition):
    class Meta:
        db_table = 'peopleposition26'


class PeoplePosition27(PeoplePosition):
    class Meta:
        db_table = 'peopleposition27'


class PeoplePosition28(PeoplePosition):
    class Meta:
        db_table = 'peopleposition28'


class PeoplePosition29(PeoplePosition):
    class Meta:
        db_table = 'peopleposition29'


class PeoplePosition30(PeoplePosition):
    class Meta:
        db_table = 'peopleposition30'


class PeoplePosition31(PeoplePosition):
    class Meta:
        db_table = 'peopleposition31'


class PeoplePosition32(PeoplePosition):
    class Meta:
        db_table = 'peopleposition32'


class PeoplePosition33(PeoplePosition):
    class Meta:
        db_table = 'peopleposition33'


class PeoplePosition34(PeoplePosition):
    class Meta:
        db_table = 'peopleposition34'


class PeoplePosition35(PeoplePosition):
    class Meta:
        db_table = 'peopleposition35'


class PeoplePosition36(PeoplePosition):
    class Meta:
        db_table = 'peopleposition36'


class PeoplePosition37(PeoplePosition):
    class Meta:
        db_table = 'peopleposition37'


class PeoplePosition38(PeoplePosition):
    class Meta:
        db_table = 'peopleposition38'


class PeoplePosition39(PeoplePosition):
    class Meta:
        db_table = 'peopleposition39'


class PeoplePosition40(PeoplePosition):
    class Meta:
        db_table = 'peopleposition40'


class PeoplePosition41(PeoplePosition):
    class Meta:
        db_table = 'peopleposition41'


class PeoplePosition42(PeoplePosition):
    class Meta:
        db_table = 'peopleposition42'


class PeoplePosition43(PeoplePosition):
    class Meta:
        db_table = 'peopleposition43'


class PeoplePosition44(PeoplePosition):
    class Meta:
        db_table = 'peopleposition44'


class PeoplePosition45(PeoplePosition):
    class Meta:
        db_table = 'peopleposition45'


class PeoplePosition46(PeoplePosition):
    class Meta:
        db_table = 'peopleposition46'


class PeoplePosition47(PeoplePosition):
    class Meta:
        db_table = 'peopleposition47'


class PeoplePosition48(PeoplePosition):
    class Meta:
        db_table = 'peopleposition48'


class PeoplePosition49(PeoplePosition):
    class Meta:
        db_table = 'peopleposition49'


class PeoplePosition50(PeoplePosition):
    class Meta:
        db_table = 'peopleposition50'


class PeoplePosition51(PeoplePosition):
    class Meta:
        db_table = 'peopleposition51'


class PeoplePosition52(PeoplePosition):
    class Meta:
        db_table = 'peopleposition52'


class PeoplePosition53(PeoplePosition):
    class Meta:
        db_table = 'peopleposition53'


class PeoplePosition54(PeoplePosition):
    class Meta:
        db_table = 'peopleposition54'


class PeoplePosition55(PeoplePosition):
    class Meta:
        db_table = 'peopleposition55'


class PeoplePosition56(PeoplePosition):
    class Meta:
        db_table = 'peopleposition56'


class PeoplePosition57(PeoplePosition):
    class Meta:
        db_table = 'peopleposition57'


class PeoplePosition58(PeoplePosition):
    class Meta:
        db_table = 'peopleposition58'


class PeoplePosition59(PeoplePosition):
    class Meta:
        db_table = 'peopleposition59'


class PeoplePosition60(PeoplePosition):
    class Meta:
        db_table = 'peopleposition60'


class PeoplePosition61(PeoplePosition):
    class Meta:
        db_table = 'peopleposition61'


class PeoplePosition62(PeoplePosition):
    class Meta:
        db_table = 'peopleposition62'


class PeoplePosition63(PeoplePosition):
    class Meta:
        db_table = 'peopleposition63'


class PeoplePosition64(PeoplePosition):
    class Meta:
        db_table = 'peopleposition64'


class PeoplePosition65(PeoplePosition):
    class Meta:
        db_table = 'peopleposition65'


class PeoplePosition66(PeoplePosition):
    class Meta:
        db_table = 'peopleposition66'


class PeoplePosition67(PeoplePosition):
    class Meta:
        db_table = 'peopleposition67'


class PeoplePosition68(PeoplePosition):
    class Meta:
        db_table = 'peopleposition68'


class PeoplePosition69(PeoplePosition):
    class Meta:
        db_table = 'peopleposition69'


class PeoplePosition70(PeoplePosition):
    class Meta:
        db_table = 'peopleposition70'


class PeoplePosition71(PeoplePosition):
    class Meta:
        db_table = 'peopleposition71'


class PeoplePosition72(PeoplePosition):
    class Meta:
        db_table = 'peopleposition72'


class PeoplePosition73(PeoplePosition):
    class Meta:
        db_table = 'peopleposition73'


class PeoplePosition74(PeoplePosition):
    class Meta:
        db_table = 'peopleposition74'


class PeoplePosition75(PeoplePosition):
    class Meta:
        db_table = 'peopleposition75'


class PeoplePosition76(PeoplePosition):
    class Meta:
        db_table = 'peopleposition76'


class PeoplePosition77(PeoplePosition):
    class Meta:
        db_table = 'peopleposition77'


class PeoplePosition78(PeoplePosition):
    class Meta:
        db_table = 'peopleposition78'


class PeoplePosition79(PeoplePosition):
    class Meta:
        db_table = 'peopleposition79'


class PeoplePosition80(PeoplePosition):
    class Meta:
        db_table = 'peopleposition80'


class PeoplePosition81(PeoplePosition):
    class Meta:
        db_table = 'peopleposition81'


class PeoplePosition82(PeoplePosition):
    class Meta:
        db_table = 'peopleposition82'


class PeoplePosition83(PeoplePosition):
    class Meta:
        db_table = 'peopleposition83'


class PeoplePosition84(PeoplePosition):
    class Meta:
        db_table = 'peopleposition84'


class PeoplePosition85(PeoplePosition):
    class Meta:
        db_table = 'peopleposition85'


class PeoplePosition86(PeoplePosition):
    class Meta:
        db_table = 'peopleposition86'


class PeoplePosition87(PeoplePosition):
    class Meta:
        db_table = 'peopleposition87'


class PeoplePosition88(PeoplePosition):
    class Meta:
        db_table = 'peopleposition88'


class PeoplePosition89(PeoplePosition):
    class Meta:
        db_table = 'peopleposition89'


class PeoplePosition90(PeoplePosition):
    class Meta:
        db_table = 'peopleposition90'


class PeoplePosition91(PeoplePosition):
    class Meta:
        db_table = 'peopleposition91'


class PeoplePosition92(PeoplePosition):
    class Meta:
        db_table = 'peopleposition92'


class PeoplePosition93(PeoplePosition):
    class Meta:
        db_table = 'peopleposition93'


class PeoplePosition94(PeoplePosition):
    class Meta:
        db_table = 'peopleposition94'


class PeoplePosition95(PeoplePosition):
    class Meta:
        db_table = 'peopleposition95'


class PeoplePosition96(PeoplePosition):
    class Meta:
        db_table = 'peopleposition96'


class PeoplePosition97(PeoplePosition):
    class Meta:
        db_table = 'peopleposition97'


class PeoplePosition98(PeoplePosition):
    class Meta:
        db_table = 'peopleposition98'


class PeoplePosition99(PeoplePosition):
    class Meta:
        db_table = 'peopleposition99'


class PeoplePosition100(PeoplePosition):
    class Meta:
        db_table = 'peopleposition100'


class PeoplePosition101(PeoplePosition):
    class Meta:
        db_table = 'peopleposition101'


class PeoplePosition102(PeoplePosition):
    class Meta:
        db_table = 'peopleposition102'


class PeoplePosition103(PeoplePosition):
    class Meta:
        db_table = 'peopleposition103'


class PeoplePosition104(PeoplePosition):
    class Meta:
        db_table = 'peopleposition104'


class PeoplePosition105(PeoplePosition):
    class Meta:
        db_table = 'peopleposition105'


class PeoplePosition106(PeoplePosition):
    class Meta:
        db_table = 'peopleposition106'


class PeoplePosition107(PeoplePosition):
    class Meta:
        db_table = 'peopleposition107'


class PeoplePosition108(PeoplePosition):
    class Meta:
        db_table = 'peopleposition108'


class PeoplePosition109(PeoplePosition):
    class Meta:
        db_table = 'peopleposition109'


class PeoplePosition110(PeoplePosition):
    class Meta:
        db_table = 'peopleposition110'


class PeoplePosition111(PeoplePosition):
    class Meta:
        db_table = 'peopleposition111'


class PeoplePosition112(PeoplePosition):
    class Meta:
        db_table = 'peopleposition112'


class PeoplePosition113(PeoplePosition):
    class Meta:
        db_table = 'peopleposition113'


class PeoplePosition114(PeoplePosition):
    class Meta:
        db_table = 'peopleposition114'


class PeoplePosition115(PeoplePosition):
    class Meta:
        db_table = 'peopleposition115'


class PeoplePosition116(PeoplePosition):
    class Meta:
        db_table = 'peopleposition116'


class PeoplePosition117(PeoplePosition):
    class Meta:
        db_table = 'peopleposition117'


class PeoplePosition118(PeoplePosition):
    class Meta:
        db_table = 'peopleposition118'


class PeoplePosition119(PeoplePosition):
    class Meta:
        db_table = 'peopleposition119'


class PeoplePosition120(PeoplePosition):
    class Meta:
        db_table = 'peopleposition120'


class PeoplePosition121(PeoplePosition):
    class Meta:
        db_table = 'peopleposition121'


class PeoplePosition122(PeoplePosition):
    class Meta:
        db_table = 'peopleposition122'


class PeoplePosition123(PeoplePosition):
    class Meta:
        db_table = 'peopleposition123'


class PeoplePosition124(PeoplePosition):
    class Meta:
        db_table = 'peopleposition124'


class PeoplePosition125(PeoplePosition):
    class Meta:
        db_table = 'peopleposition125'


class PeoplePosition126(PeoplePosition):
    class Meta:
        db_table = 'peopleposition126'


class PeoplePosition127(PeoplePosition):
    class Meta:
        db_table = 'peopleposition127'


class PeoplePosition128(PeoplePosition):
    class Meta:
        db_table = 'peopleposition128'


class PeoplePosition129(PeoplePosition):
    class Meta:
        db_table = 'peopleposition129'


class PeoplePosition130(PeoplePosition):
    class Meta:
        db_table = 'peopleposition130'


class PeoplePosition131(PeoplePosition):
    class Meta:
        db_table = 'peopleposition131'


class PeoplePosition132(PeoplePosition):
    class Meta:
        db_table = 'peopleposition132'


class PeoplePosition133(PeoplePosition):
    class Meta:
        db_table = 'peopleposition133'


class PeoplePosition134(PeoplePosition):
    class Meta:
        db_table = 'peopleposition134'


class PeoplePosition135(PeoplePosition):
    class Meta:
        db_table = 'peopleposition135'


class PeoplePosition136(PeoplePosition):
    class Meta:
        db_table = 'peopleposition136'


class PeoplePosition137(PeoplePosition):
    class Meta:
        db_table = 'peopleposition137'


class PeoplePosition138(PeoplePosition):
    class Meta:
        db_table = 'peopleposition138'


class PeoplePosition139(PeoplePosition):
    class Meta:
        db_table = 'peopleposition139'


class PeoplePosition140(PeoplePosition):
    class Meta:
        db_table = 'peopleposition140'


class PeoplePosition141(PeoplePosition):
    class Meta:
        db_table = 'peopleposition141'


class PeoplePosition142(PeoplePosition):
    class Meta:
        db_table = 'peopleposition142'


class PeoplePosition143(PeoplePosition):
    class Meta:
        db_table = 'peopleposition143'


class PeoplePosition144(PeoplePosition):
    class Meta:
        db_table = 'peopleposition144'


class PeoplePosition145(PeoplePosition):
    class Meta:
        db_table = 'peopleposition145'


class PeoplePosition146(PeoplePosition):
    class Meta:
        db_table = 'peopleposition146'


class PeoplePosition147(PeoplePosition):
    class Meta:
        db_table = 'peopleposition147'


class PeoplePosition148(PeoplePosition):
    class Meta:
        db_table = 'peopleposition148'


class PeoplePosition149(PeoplePosition):
    class Meta:
        db_table = 'peopleposition149'


class PeoplePosition150(PeoplePosition):
    class Meta:
        db_table = 'peopleposition150'


class PeoplePosition151(PeoplePosition):
    class Meta:
        db_table = 'peopleposition151'


class PeoplePosition152(PeoplePosition):
    class Meta:
        db_table = 'peopleposition152'


class PeoplePosition153(PeoplePosition):
    class Meta:
        db_table = 'peopleposition153'


class PeoplePosition154(PeoplePosition):
    class Meta:
        db_table = 'peopleposition154'


class PeoplePosition155(PeoplePosition):
    class Meta:
        db_table = 'peopleposition155'


class PeoplePosition156(PeoplePosition):
    class Meta:
        db_table = 'peopleposition156'


class PeoplePosition157(PeoplePosition):
    class Meta:
        db_table = 'peopleposition157'


class PeoplePosition158(PeoplePosition):
    class Meta:
        db_table = 'peopleposition158'


class PeoplePosition159(PeoplePosition):
    class Meta:
        db_table = 'peopleposition159'


class PeoplePosition160(PeoplePosition):
    class Meta:
        db_table = 'peopleposition160'


class PeoplePosition161(PeoplePosition):
    class Meta:
        db_table = 'peopleposition161'


class PeoplePosition162(PeoplePosition):
    class Meta:
        db_table = 'peopleposition162'


class PeoplePosition163(PeoplePosition):
    class Meta:
        db_table = 'peopleposition163'


class PeoplePosition164(PeoplePosition):
    class Meta:
        db_table = 'peopleposition164'


class PeoplePosition165(PeoplePosition):
    class Meta:
        db_table = 'peopleposition165'


class PeoplePosition166(PeoplePosition):
    class Meta:
        db_table = 'peopleposition166'


class PeoplePosition167(PeoplePosition):
    class Meta:
        db_table = 'peopleposition167'


class PeoplePosition168(PeoplePosition):
    class Meta:
        db_table = 'peopleposition168'


class PeoplePosition169(PeoplePosition):
    class Meta:
        db_table = 'peopleposition169'


class PeoplePosition170(PeoplePosition):
    class Meta:
        db_table = 'peopleposition170'


class PeoplePosition171(PeoplePosition):
    class Meta:
        db_table = 'peopleposition171'


class PeoplePosition172(PeoplePosition):
    class Meta:
        db_table = 'peopleposition172'


class PeoplePosition173(PeoplePosition):
    class Meta:
        db_table = 'peopleposition173'


class PeoplePosition174(PeoplePosition):
    class Meta:
        db_table = 'peopleposition174'


class PeoplePosition175(PeoplePosition):
    class Meta:
        db_table = 'peopleposition175'


class PeoplePosition176(PeoplePosition):
    class Meta:
        db_table = 'peopleposition176'


class PeoplePosition177(PeoplePosition):
    class Meta:
        db_table = 'peopleposition177'


class PeoplePosition178(PeoplePosition):
    class Meta:
        db_table = 'peopleposition178'


class PeoplePosition179(PeoplePosition):
    class Meta:
        db_table = 'peopleposition179'


class PeoplePosition180(PeoplePosition):
    class Meta:
        db_table = 'peopleposition180'


class PeoplePosition181(PeoplePosition):
    class Meta:
        db_table = 'peopleposition181'


class PeoplePosition182(PeoplePosition):
    class Meta:
        db_table = 'peopleposition182'


class PeoplePosition183(PeoplePosition):
    class Meta:
        db_table = 'peopleposition183'


class PeoplePosition184(PeoplePosition):
    class Meta:
        db_table = 'peopleposition184'


class PeoplePosition185(PeoplePosition):
    class Meta:
        db_table = 'peopleposition185'


class PeoplePosition186(PeoplePosition):
    class Meta:
        db_table = 'peopleposition186'


class PeoplePosition187(PeoplePosition):
    class Meta:
        db_table = 'peopleposition187'


class PeoplePosition188(PeoplePosition):
    class Meta:
        db_table = 'peopleposition188'


class PeoplePosition189(PeoplePosition):
    class Meta:
        db_table = 'peopleposition189'


class PeoplePosition190(PeoplePosition):
    class Meta:
        db_table = 'peopleposition190'


class PeoplePosition191(PeoplePosition):
    class Meta:
        db_table = 'peopleposition191'


class PeoplePosition192(PeoplePosition):
    class Meta:
        db_table = 'peopleposition192'


class PeoplePosition193(PeoplePosition):
    class Meta:
        db_table = 'peopleposition193'


class PeoplePosition194(PeoplePosition):
    class Meta:
        db_table = 'peopleposition194'


class PeoplePosition195(PeoplePosition):
    class Meta:
        db_table = 'peopleposition195'


class PeoplePosition196(PeoplePosition):
    class Meta:
        db_table = 'peopleposition196'


class PeoplePosition197(PeoplePosition):
    class Meta:
        db_table = 'peopleposition197'


class PeoplePosition198(PeoplePosition):
    class Meta:
        db_table = 'peopleposition198'


class PeoplePosition199(PeoplePosition):
    class Meta:
        db_table = 'peopleposition199'


class PeoplePosition200(PeoplePosition):
    class Meta:
        db_table = 'peopleposition200'


class PeoplePosition201(PeoplePosition):
    class Meta:
        db_table = 'peopleposition201'


class PeoplePosition202(PeoplePosition):
    class Meta:
        db_table = 'peopleposition202'


class PeoplePosition203(PeoplePosition):
    class Meta:
        db_table = 'peopleposition203'


class PeoplePosition204(PeoplePosition):
    class Meta:
        db_table = 'peopleposition204'


class PeoplePosition205(PeoplePosition):
    class Meta:
        db_table = 'peopleposition205'


class PeoplePosition206(PeoplePosition):
    class Meta:
        db_table = 'peopleposition206'


class PeoplePosition207(PeoplePosition):
    class Meta:
        db_table = 'peopleposition207'


class PeoplePosition208(PeoplePosition):
    class Meta:
        db_table = 'peopleposition208'


class PeoplePosition209(PeoplePosition):
    class Meta:
        db_table = 'peopleposition209'


class PeoplePosition210(PeoplePosition):
    class Meta:
        db_table = 'peopleposition210'


class PeoplePosition211(PeoplePosition):
    class Meta:
        db_table = 'peopleposition211'


class PeoplePosition212(PeoplePosition):
    class Meta:
        db_table = 'peopleposition212'


class PeoplePosition213(PeoplePosition):
    class Meta:
        db_table = 'peopleposition213'


class PeoplePosition214(PeoplePosition):
    class Meta:
        db_table = 'peopleposition214'


class PeoplePosition215(PeoplePosition):
    class Meta:
        db_table = 'peopleposition215'


class PeoplePosition216(PeoplePosition):
    class Meta:
        db_table = 'peopleposition216'


class PeoplePosition217(PeoplePosition):
    class Meta:
        db_table = 'peopleposition217'


class PeoplePosition218(PeoplePosition):
    class Meta:
        db_table = 'peopleposition218'


class PeoplePosition219(PeoplePosition):
    class Meta:
        db_table = 'peopleposition219'


class PeoplePosition220(PeoplePosition):
    class Meta:
        db_table = 'peopleposition220'


class PeoplePosition221(PeoplePosition):
    class Meta:
        db_table = 'peopleposition221'


class PeoplePosition222(PeoplePosition):
    class Meta:
        db_table = 'peopleposition222'


class PeoplePosition223(PeoplePosition):
    class Meta:
        db_table = 'peopleposition223'


class PeoplePosition224(PeoplePosition):
    class Meta:
        db_table = 'peopleposition224'


class PeoplePosition225(PeoplePosition):
    class Meta:
        db_table = 'peopleposition225'


class PeoplePosition226(PeoplePosition):
    class Meta:
        db_table = 'peopleposition226'


class PeoplePosition227(PeoplePosition):
    class Meta:
        db_table = 'peopleposition227'


class PeoplePosition228(PeoplePosition):
    class Meta:
        db_table = 'peopleposition228'


class PeoplePosition229(PeoplePosition):
    class Meta:
        db_table = 'peopleposition229'


class PeoplePosition230(PeoplePosition):
    class Meta:
        db_table = 'peopleposition230'


class PeoplePosition231(PeoplePosition):
    class Meta:
        db_table = 'peopleposition231'


class PeoplePosition232(PeoplePosition):
    class Meta:
        db_table = 'peopleposition232'


class PeoplePosition233(PeoplePosition):
    class Meta:
        db_table = 'peopleposition233'


class PeoplePosition234(PeoplePosition):
    class Meta:
        db_table = 'peopleposition234'


class PeoplePosition235(PeoplePosition):
    class Meta:
        db_table = 'peopleposition235'


class PeoplePosition236(PeoplePosition):
    class Meta:
        db_table = 'peopleposition236'


class PeoplePosition237(PeoplePosition):
    class Meta:
        db_table = 'peopleposition237'


class PeoplePosition238(PeoplePosition):
    class Meta:
        db_table = 'peopleposition238'


class PeoplePosition239(PeoplePosition):
    class Meta:
        db_table = 'peopleposition239'


class PeoplePosition240(PeoplePosition):
    class Meta:
        db_table = 'peopleposition240'


class PeoplePosition241(PeoplePosition):
    class Meta:
        db_table = 'peopleposition241'


class PeoplePosition242(PeoplePosition):
    class Meta:
        db_table = 'peopleposition242'


class PeoplePosition243(PeoplePosition):
    class Meta:
        db_table = 'peopleposition243'


class PeoplePosition244(PeoplePosition):
    class Meta:
        db_table = 'peopleposition244'


class PeoplePosition245(PeoplePosition):
    class Meta:
        db_table = 'peopleposition245'


class PeoplePosition246(PeoplePosition):
    class Meta:
        db_table = 'peopleposition246'


class PeoplePosition247(PeoplePosition):
    class Meta:
        db_table = 'peopleposition247'


class PeoplePosition248(PeoplePosition):
    class Meta:
        db_table = 'peopleposition248'


class PeoplePosition249(PeoplePosition):
    class Meta:
        db_table = 'peopleposition249'


class PeoplePosition250(PeoplePosition):
    class Meta:
        db_table = 'peopleposition250'


class PeoplePosition251(PeoplePosition):
    class Meta:
        db_table = 'peopleposition251'


class PeoplePosition252(PeoplePosition):
    class Meta:
        db_table = 'peopleposition252'


class PeoplePosition253(PeoplePosition):
    class Meta:
        db_table = 'peopleposition253'


class PeoplePosition254(PeoplePosition):
    class Meta:
        db_table = 'peopleposition254'


class PeoplePosition255(PeoplePosition):
    class Meta:
        db_table = 'peopleposition255'


class PeoplePosition256(PeoplePosition):
    class Meta:
        db_table = 'peopleposition256'


class PeoplePosition257(PeoplePosition):
    class Meta:
        db_table = 'peopleposition257'


class PeoplePosition258(PeoplePosition):
    class Meta:
        db_table = 'peopleposition258'


class PeoplePosition259(PeoplePosition):
    class Meta:
        db_table = 'peopleposition259'


class PeoplePosition260(PeoplePosition):
    class Meta:
        db_table = 'peopleposition260'


class PeoplePosition261(PeoplePosition):
    class Meta:
        db_table = 'peopleposition261'


class PeoplePosition262(PeoplePosition):
    class Meta:
        db_table = 'peopleposition262'


class PeoplePosition263(PeoplePosition):
    class Meta:
        db_table = 'peopleposition263'


class PeoplePosition264(PeoplePosition):
    class Meta:
        db_table = 'peopleposition264'


class PeoplePosition265(PeoplePosition):
    class Meta:
        db_table = 'peopleposition265'


class PeoplePosition266(PeoplePosition):
    class Meta:
        db_table = 'peopleposition266'


class PeoplePosition267(PeoplePosition):
    class Meta:
        db_table = 'peopleposition267'


class PeoplePosition268(PeoplePosition):
    class Meta:
        db_table = 'peopleposition268'


class PeoplePosition269(PeoplePosition):
    class Meta:
        db_table = 'peopleposition269'


class PeoplePosition270(PeoplePosition):
    class Meta:
        db_table = 'peopleposition270'


class PeoplePosition271(PeoplePosition):
    class Meta:
        db_table = 'peopleposition271'


class PeoplePosition272(PeoplePosition):
    class Meta:
        db_table = 'peopleposition272'


class PeoplePosition273(PeoplePosition):
    class Meta:
        db_table = 'peopleposition273'


class PeoplePosition274(PeoplePosition):
    class Meta:
        db_table = 'peopleposition274'


class PeoplePosition275(PeoplePosition):
    class Meta:
        db_table = 'peopleposition275'


class PeoplePosition276(PeoplePosition):
    class Meta:
        db_table = 'peopleposition276'


class PeoplePosition277(PeoplePosition):
    class Meta:
        db_table = 'peopleposition277'


class PeoplePosition278(PeoplePosition):
    class Meta:
        db_table = 'peopleposition278'


class PeoplePosition279(PeoplePosition):
    class Meta:
        db_table = 'peopleposition279'


class PeoplePosition280(PeoplePosition):
    class Meta:
        db_table = 'peopleposition280'


class PeoplePosition281(PeoplePosition):
    class Meta:
        db_table = 'peopleposition281'


class PeoplePosition282(PeoplePosition):
    class Meta:
        db_table = 'peopleposition282'


class PeoplePosition283(PeoplePosition):
    class Meta:
        db_table = 'peopleposition283'


class PeoplePosition284(PeoplePosition):
    class Meta:
        db_table = 'peopleposition284'


class PeoplePosition285(PeoplePosition):
    class Meta:
        db_table = 'peopleposition285'


class PeoplePosition286(PeoplePosition):
    class Meta:
        db_table = 'peopleposition286'


class PeoplePosition287(PeoplePosition):
    class Meta:
        db_table = 'peopleposition287'


class PeoplePosition288(PeoplePosition):
    class Meta:
        db_table = 'peopleposition288'


class PeoplePosition289(PeoplePosition):
    class Meta:
        db_table = 'peopleposition289'


class PeoplePosition290(PeoplePosition):
    class Meta:
        db_table = 'peopleposition290'


class PeoplePosition291(PeoplePosition):
    class Meta:
        db_table = 'peopleposition291'


class PeoplePosition292(PeoplePosition):
    class Meta:
        db_table = 'peopleposition292'


class PeoplePosition293(PeoplePosition):
    class Meta:
        db_table = 'peopleposition293'


class PeoplePosition294(PeoplePosition):
    class Meta:
        db_table = 'peopleposition294'


class PeoplePosition295(PeoplePosition):
    class Meta:
        db_table = 'peopleposition295'


class PeoplePosition296(PeoplePosition):
    class Meta:
        db_table = 'peopleposition296'


class PeoplePosition297(PeoplePosition):
    class Meta:
        db_table = 'peopleposition297'


class PeoplePosition298(PeoplePosition):
    class Meta:
        db_table = 'peopleposition298'


class PeoplePosition299(PeoplePosition):
    class Meta:
        db_table = 'peopleposition299'


class PeoplePosition300(PeoplePosition):
    class Meta:
        db_table = 'peopleposition300'


class PeoplePosition301(PeoplePosition):
    class Meta:
        db_table = 'peopleposition301'


class PeoplePosition302(PeoplePosition):
    class Meta:
        db_table = 'peopleposition302'


class PeoplePosition303(PeoplePosition):
    class Meta:
        db_table = 'peopleposition303'


class PeoplePosition304(PeoplePosition):
    class Meta:
        db_table = 'peopleposition304'


class PeoplePosition305(PeoplePosition):
    class Meta:
        db_table = 'peopleposition305'


class PeoplePosition306(PeoplePosition):
    class Meta:
        db_table = 'peopleposition306'


class PeoplePosition307(PeoplePosition):
    class Meta:
        db_table = 'peopleposition307'


class PeoplePosition308(PeoplePosition):
    class Meta:
        db_table = 'peopleposition308'


class PeoplePosition309(PeoplePosition):
    class Meta:
        db_table = 'peopleposition309'


class PeoplePosition310(PeoplePosition):
    class Meta:
        db_table = 'peopleposition310'


class PeoplePosition311(PeoplePosition):
    class Meta:
        db_table = 'peopleposition311'


class PeoplePosition312(PeoplePosition):
    class Meta:
        db_table = 'peopleposition312'


class PeoplePosition313(PeoplePosition):
    class Meta:
        db_table = 'peopleposition313'


class PeoplePosition314(PeoplePosition):
    class Meta:
        db_table = 'peopleposition314'


class PeoplePosition315(PeoplePosition):
    class Meta:
        db_table = 'peopleposition315'


class PeoplePosition316(PeoplePosition):
    class Meta:
        db_table = 'peopleposition316'


class PeoplePosition317(PeoplePosition):
    class Meta:
        db_table = 'peopleposition317'


class PeoplePosition318(PeoplePosition):
    class Meta:
        db_table = 'peopleposition318'


class PeoplePosition319(PeoplePosition):
    class Meta:
        db_table = 'peopleposition319'


class PeoplePosition320(PeoplePosition):
    class Meta:
        db_table = 'peopleposition320'


class PeoplePosition321(PeoplePosition):
    class Meta:
        db_table = 'peopleposition321'


class PeoplePosition322(PeoplePosition):
    class Meta:
        db_table = 'peopleposition322'


class PeoplePosition323(PeoplePosition):
    class Meta:
        db_table = 'peopleposition323'


class PeoplePosition324(PeoplePosition):
    class Meta:
        db_table = 'peopleposition324'


class PeoplePosition325(PeoplePosition):
    class Meta:
        db_table = 'peopleposition325'


class PeoplePosition326(PeoplePosition):
    class Meta:
        db_table = 'peopleposition326'


class PeoplePosition327(PeoplePosition):
    class Meta:
        db_table = 'peopleposition327'


class PeoplePosition328(PeoplePosition):
    class Meta:
        db_table = 'peopleposition328'


class PeoplePosition329(PeoplePosition):
    class Meta:
        db_table = 'peopleposition329'


class PeoplePosition330(PeoplePosition):
    class Meta:
        db_table = 'peopleposition330'


class PeoplePosition331(PeoplePosition):
    class Meta:
        db_table = 'peopleposition331'


class PeoplePosition332(PeoplePosition):
    class Meta:
        db_table = 'peopleposition332'


class PeoplePosition333(PeoplePosition):
    class Meta:
        db_table = 'peopleposition333'


class PeoplePosition334(PeoplePosition):
    class Meta:
        db_table = 'peopleposition334'


class PeoplePosition335(PeoplePosition):
    class Meta:
        db_table = 'peopleposition335'


class PeoplePosition336(PeoplePosition):
    class Meta:
        db_table = 'peopleposition336'


class PeoplePosition337(PeoplePosition):
    class Meta:
        db_table = 'peopleposition337'


class PeoplePosition338(PeoplePosition):
    class Meta:
        db_table = 'peopleposition338'


class PeoplePosition339(PeoplePosition):
    class Meta:
        db_table = 'peopleposition339'


class PeoplePosition340(PeoplePosition):
    class Meta:
        db_table = 'peopleposition340'


class PeoplePosition341(PeoplePosition):
    class Meta:
        db_table = 'peopleposition341'


class PeoplePosition342(PeoplePosition):
    class Meta:
        db_table = 'peopleposition342'


class PeoplePosition343(PeoplePosition):
    class Meta:
        db_table = 'peopleposition343'


class PeoplePosition344(PeoplePosition):
    class Meta:
        db_table = 'peopleposition344'


class PeoplePosition345(PeoplePosition):
    class Meta:
        db_table = 'peopleposition345'


class PeoplePosition346(PeoplePosition):
    class Meta:
        db_table = 'peopleposition346'


class PeoplePosition347(PeoplePosition):
    class Meta:
        db_table = 'peopleposition347'


class PeoplePosition348(PeoplePosition):
    class Meta:
        db_table = 'peopleposition348'


class PeoplePosition349(PeoplePosition):
    class Meta:
        db_table = 'peopleposition349'


class PeoplePosition350(PeoplePosition):
    class Meta:
        db_table = 'peopleposition350'


class PeoplePosition351(PeoplePosition):
    class Meta:
        db_table = 'peopleposition351'


class PeoplePosition352(PeoplePosition):
    class Meta:
        db_table = 'peopleposition352'


class PeoplePosition353(PeoplePosition):
    class Meta:
        db_table = 'peopleposition353'


class PeoplePosition354(PeoplePosition):
    class Meta:
        db_table = 'peopleposition354'


class PeoplePosition355(PeoplePosition):
    class Meta:
        db_table = 'peopleposition355'


class PeoplePosition356(PeoplePosition):
    class Meta:
        db_table = 'peopleposition356'


class PeoplePosition357(PeoplePosition):
    class Meta:
        db_table = 'peopleposition357'


class PeoplePosition358(PeoplePosition):
    class Meta:
        db_table = 'peopleposition358'


class PeoplePosition359(PeoplePosition):
    class Meta:
        db_table = 'peopleposition359'


class PeoplePosition360(PeoplePosition):
    class Meta:
        db_table = 'peopleposition360'


class PeoplePosition361(PeoplePosition):
    class Meta:
        db_table = 'peopleposition361'


class PeoplePosition362(PeoplePosition):
    class Meta:
        db_table = 'peopleposition362'


class PeoplePosition363(PeoplePosition):
    class Meta:
        db_table = 'peopleposition363'


class PeoplePosition364(PeoplePosition):
    class Meta:
        db_table = 'peopleposition364'


class PeoplePosition365(PeoplePosition):
    class Meta:
        db_table = 'peopleposition365'


class PeoplePosition366(PeoplePosition):
    class Meta:
        db_table = 'peopleposition366'


class PeoplePosition367(PeoplePosition):
    class Meta:
        db_table = 'peopleposition367'


class PeoplePosition368(PeoplePosition):
    class Meta:
        db_table = 'peopleposition368'


class PeoplePosition369(PeoplePosition):
    class Meta:
        db_table = 'peopleposition369'


class PeoplePosition370(PeoplePosition):
    class Meta:
        db_table = 'peopleposition370'


class PeoplePosition371(PeoplePosition):
    class Meta:
        db_table = 'peopleposition371'


class PeoplePosition372(PeoplePosition):
    class Meta:
        db_table = 'peopleposition372'


class PeoplePosition373(PeoplePosition):
    class Meta:
        db_table = 'peopleposition373'


class PeoplePosition374(PeoplePosition):
    class Meta:
        db_table = 'peopleposition374'


class PeoplePosition375(PeoplePosition):
    class Meta:
        db_table = 'peopleposition375'


class PeoplePosition376(PeoplePosition):
    class Meta:
        db_table = 'peopleposition376'


class PeoplePosition377(PeoplePosition):
    class Meta:
        db_table = 'peopleposition377'


class PeoplePosition378(PeoplePosition):
    class Meta:
        db_table = 'peopleposition378'


class PeoplePosition379(PeoplePosition):
    class Meta:
        db_table = 'peopleposition379'


class PeoplePosition380(PeoplePosition):
    class Meta:
        db_table = 'peopleposition380'


class PeoplePosition381(PeoplePosition):
    class Meta:
        db_table = 'peopleposition381'


class PeoplePosition382(PeoplePosition):
    class Meta:
        db_table = 'peopleposition382'


class PeoplePosition383(PeoplePosition):
    class Meta:
        db_table = 'peopleposition383'


class PeoplePosition384(PeoplePosition):
    class Meta:
        db_table = 'peopleposition384'


class PeoplePosition385(PeoplePosition):
    class Meta:
        db_table = 'peopleposition385'


class PeoplePosition386(PeoplePosition):
    class Meta:
        db_table = 'peopleposition386'


class PeoplePosition387(PeoplePosition):
    class Meta:
        db_table = 'peopleposition387'


class PeoplePosition388(PeoplePosition):
    class Meta:
        db_table = 'peopleposition388'


class PeoplePosition389(PeoplePosition):
    class Meta:
        db_table = 'peopleposition389'


class PeoplePosition390(PeoplePosition):
    class Meta:
        db_table = 'peopleposition390'


class PeoplePosition391(PeoplePosition):
    class Meta:
        db_table = 'peopleposition391'


class PeoplePosition392(PeoplePosition):
    class Meta:
        db_table = 'peopleposition392'


class PeoplePosition393(PeoplePosition):
    class Meta:
        db_table = 'peopleposition393'


class PeoplePosition394(PeoplePosition):
    class Meta:
        db_table = 'peopleposition394'


class PeoplePosition395(PeoplePosition):
    class Meta:
        db_table = 'peopleposition395'


class PeoplePosition396(PeoplePosition):
    class Meta:
        db_table = 'peopleposition396'


class PeoplePosition397(PeoplePosition):
    class Meta:
        db_table = 'peopleposition397'


class PeoplePosition398(PeoplePosition):
    class Meta:
        db_table = 'peopleposition398'


class PeoplePosition399(PeoplePosition):
    class Meta:
        db_table = 'peopleposition399'


class PeoplePosition400(PeoplePosition):
    class Meta:
        db_table = 'peopleposition400'


class PeoplePosition401(PeoplePosition):
    class Meta:
        db_table = 'peopleposition401'


class PeoplePosition402(PeoplePosition):
    class Meta:
        db_table = 'peopleposition402'


class PeoplePosition403(PeoplePosition):
    class Meta:
        db_table = 'peopleposition403'


class PeoplePosition404(PeoplePosition):
    class Meta:
        db_table = 'peopleposition404'


class PeoplePosition405(PeoplePosition):
    class Meta:
        db_table = 'peopleposition405'


class PeoplePosition406(PeoplePosition):
    class Meta:
        db_table = 'peopleposition406'


class PeoplePosition407(PeoplePosition):
    class Meta:
        db_table = 'peopleposition407'


class PeoplePosition408(PeoplePosition):
    class Meta:
        db_table = 'peopleposition408'


class PeoplePosition409(PeoplePosition):
    class Meta:
        db_table = 'peopleposition409'


class PeoplePosition410(PeoplePosition):
    class Meta:
        db_table = 'peopleposition410'


class PeoplePosition411(PeoplePosition):
    class Meta:
        db_table = 'peopleposition411'


class PeoplePosition412(PeoplePosition):
    class Meta:
        db_table = 'peopleposition412'


class PeoplePosition413(PeoplePosition):
    class Meta:
        db_table = 'peopleposition413'


class PeoplePosition414(PeoplePosition):
    class Meta:
        db_table = 'peopleposition414'


class PeoplePosition415(PeoplePosition):
    class Meta:
        db_table = 'peopleposition415'


class PeoplePosition416(PeoplePosition):
    class Meta:
        db_table = 'peopleposition416'


class PeoplePosition417(PeoplePosition):
    class Meta:
        db_table = 'peopleposition417'


class PeoplePosition418(PeoplePosition):
    class Meta:
        db_table = 'peopleposition418'


class PeoplePosition419(PeoplePosition):
    class Meta:
        db_table = 'peopleposition419'


class PeoplePosition420(PeoplePosition):
    class Meta:
        db_table = 'peopleposition420'


class PeoplePosition421(PeoplePosition):
    class Meta:
        db_table = 'peopleposition421'


class PeoplePosition422(PeoplePosition):
    class Meta:
        db_table = 'peopleposition422'


class PeoplePosition423(PeoplePosition):
    class Meta:
        db_table = 'peopleposition423'


class PeoplePosition424(PeoplePosition):
    class Meta:
        db_table = 'peopleposition424'


class PeoplePosition425(PeoplePosition):
    class Meta:
        db_table = 'peopleposition425'


class PeoplePosition426(PeoplePosition):
    class Meta:
        db_table = 'peopleposition426'


class PeoplePosition427(PeoplePosition):
    class Meta:
        db_table = 'peopleposition427'


class PeoplePosition428(PeoplePosition):
    class Meta:
        db_table = 'peopleposition428'


class PeoplePosition429(PeoplePosition):
    class Meta:
        db_table = 'peopleposition429'


class PeoplePosition430(PeoplePosition):
    class Meta:
        db_table = 'peopleposition430'


class PeoplePosition431(PeoplePosition):
    class Meta:
        db_table = 'peopleposition431'


class PeoplePosition432(PeoplePosition):
    class Meta:
        db_table = 'peopleposition432'


class PeoplePosition433(PeoplePosition):
    class Meta:
        db_table = 'peopleposition433'


class PeoplePosition434(PeoplePosition):
    class Meta:
        db_table = 'peopleposition434'


class PeoplePosition435(PeoplePosition):
    class Meta:
        db_table = 'peopleposition435'


class PeoplePosition436(PeoplePosition):
    class Meta:
        db_table = 'peopleposition436'


class PeoplePosition437(PeoplePosition):
    class Meta:
        db_table = 'peopleposition437'


class PeoplePosition438(PeoplePosition):
    class Meta:
        db_table = 'peopleposition438'


class PeoplePosition439(PeoplePosition):
    class Meta:
        db_table = 'peopleposition439'


class PeoplePosition440(PeoplePosition):
    class Meta:
        db_table = 'peopleposition440'


class PeoplePosition441(PeoplePosition):
    class Meta:
        db_table = 'peopleposition441'


class PeoplePosition442(PeoplePosition):
    class Meta:
        db_table = 'peopleposition442'


class PeoplePosition443(PeoplePosition):
    class Meta:
        db_table = 'peopleposition443'
