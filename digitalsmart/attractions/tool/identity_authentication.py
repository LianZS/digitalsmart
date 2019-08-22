import requests
from bs4 import BeautifulSoup


class Person:
    __slots__ = ["idcard", "area", "phone", "bir", "lunar", "gender", "latlon"]

    def __init__(self, idcard, area, phone, bir, lunar, gender, latlon):
        self.idcard: int = idcard  # 身份证号码
        self.area: str = area  # 发证地区
        self.phone: str = phone  # 电话区号
        self.bir: str = bir  # 出生日期
        self.lunar: str = lunar  # 农历
        self.gender: str = gender  # 性别/生肖
        self.latlon: tuple = latlon  # 当地经纬度

    def __str__(self):
        return "身份证号码: {0}, 发证地区: {1}, 电话区号: {2},出生日期: {3}, 农历: {4}, 性别/生肖: {5},当地经纬度:{6}".format(
            self.idcard, self.area, self.phone, self.bir, self.lunar, self.gender, self.latlon
        )


class IdentityAuthentication:
    """
    身份证信息认证
    """
    __slots__ = ['headers']
    instanceflag = 0
    instance = None

    def __new__(cls, *args, **kwargs):
        if not IdentityAuthentication.instance:
            instan = super().__new__(cls)
            IdentityAuthentication.instance = instan

            return instan
        return IdentityAuthentication.instance

    def __init__(self):
        if not IdentityAuthentication.instanceflag:
            IdentityAuthentication.instanceflag = 1
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/75.0.3770.142 Safari/537.36',
            }

    def check(self, idcard) -> Person:
        """

        :param idcard:
        :return: {'身份证号码': '440514199804220817'}, {'发证地区': '广东省  汕头市 潮南区'}, {'电话区号': '0754'},
        {'出生日期': '1998年04月22日'}, {'农历': '一九九八年三月廿六'}, {'性别/生肖': '男 (21岁)  属虎'},
        {'当地经纬度': '23.366860,116.542328'}
        """
        href = 'http://www.gpsspg.com/sfz/?q=' + str(idcard)
        response = requests.get(url=href, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        info = soup.find_all(name='tr')
        data = list()
        for item in info:
            flag = 0
            key = None
            value = None
            for itemdic in item.find_all(name='td'):
                if flag == 0:
                    key = itemdic.string
                    if not key:
                        break
                if flag == 1:
                    value = itemdic.string
                    if not value:
                        return None
                    flag = 0

                    data.append({key: value})
                    key = None
                    value = None
                    continue

                flag += 1
        idcard = area = phone = lunar = bir = gender = latlon = None
        for i in range(len(data)):
            if i == 0:
                try:
                    idcard = int(data[i].get("身份证号码"))  # 假身份证
                except Exception:
                    return None

            if i == 1:
                area = str(data[i].get("发证地区"))
            if i == 2:
                phone = str(data[i].get("电话区号"))
            if i == 3:
                bir = str(data[i].get("出生日期"))
            if i == 4:
                lunar = str(data[i].get("农历"))
            if i == 5:
                gender = str(data[i].get("性别/生肖"))
            if i == 6:
                latlon = eval(data[i].get("当地经纬度"))
        person = Person(idcard, area, phone, bir, lunar, gender, latlon)
        return person
