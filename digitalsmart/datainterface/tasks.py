import json
import requests
import re
from typing import Dict, Iterator, ByteString, Set
from urllib.parse import urlencode
from bs4 import BeautifulSoup

from digitalsmart.celeryconfig import app


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


class NetWorker(object):
    instanceflag = 0
    instance = None

    def __new__(cls, *args, **kwargs):
        if NetWorker.instance is None:
            NetWorker.instance = super().__new__(cls)
        return NetWorker.instance

    def __init__(self):

        if not NetWorker.instanceflag:
            self.headers = dict()  # 网络爬虫请求头
            self.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ' \
                                         '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

    # @app.task(queue="distribution",bind=True)
    def get_scence_distribution_data(self, pid, ddate, ttime):
        self.headers['Host'] = 'heat.qq.com'
        paramer = {
            'region_id': pid,
            'datetime': "".join([str(ddate), ' ', str(ttime)]),
            'sub_domain': ''
        }

        url = "https://heat.qq.com/api/getHeatDataByTime.php?" + urlencode(paramer)

        try:
            response = requests.get(url=url, headers=self.headers)
        except requests.exceptions.ConnectionError as e:
            return {"status": 0, "message": "本次请求失败，请重试"}
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            return {"status": 0, "message": "本次请求失败，请重试"}

    def get_idcard_info(self, idcard) -> Person:
        """
         身份证认证
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

    def get_music_list(self, name, soft_type='netease') -> Iterator[Dict]:
        """
        获所有与之相关的音乐
        :param name: 音乐名
        :param soft_type:软件类型，默认网易云，
                                netease：网易云，qq：qq音乐，kugou：酷狗音乐，kuwo：酷我，
                                xiami：虾米，baidu：百度，1ting：一听，migu：咪咕，lizhi：荔枝，
                                qingting：蜻蜓，ximalaya：喜马拉雅，kg：全民K歌，5singyc：5sing原创，
                                5singfc：5sing翻唱

        :return:
        """
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        url = "http://music.cccyun.cc/"
        paramer = {
            "input": name,
            "filter": 'name',
            'type': soft_type,
            'page': 1
        }
        response = requests.post(url=url, data=paramer, headers=self.headers)
        g = json.loads(response.text)
        music_list = g['data']
        for item in music_list:
            author = item['author']
            url = item['url']
            title = item['title']
            yield {"author": author, "url": url, "title": title}

    def down_music_content(self, url) -> Iterator[ByteString]:
        """
        下载音乐
        :param url:下载音乐链接
        :return:
        """
        response = requests.get(url=url, stream=True)
        for fragment in response.iter_content(chunk_size=1024):
            yield fragment

    def down_baidu_doc(self, url, filetype) -> Iterator[ByteString]:
        """
        下载百度文档
        :param url: 文档链接
        :param filetype: 下载类型，可选doc，pdf，ppt
        :return:
        """
        paramer = {
            "url": url,
            "type": filetype,
        }
        url = "http://wenku.baiduvvv.com/ds.php?" + urlencode(paramer)
        response = requests.get(url=url, headers=self.headers)  # 获取域名
        g = json.loads(response.text)
        domain = g['s']  # 域名
        paramer = {
            "url": url,
            "type": filetype,
            "btype": "down"

        }

        url = domain + "/wkc.php?" + urlencode(paramer)  # 下载链接
        response = requests.get(url=url, stream=True, headers=self.headers)
        for fragment in response.iter_content(chunk_size=1024):
            yield fragment

    def get_goods_price_change(self, url) -> Iterator[Set]:
        """
        获取某商品的价格变化情况
        支持天猫(detail.tmall.com、detail.m.tmall.com)、淘宝(item.taobao.com、h5.m.taobao.com)、
        京东(item.jd.com、item.m.jd.com)、一号店(item.yhd.com）、苏宁易购(product.suning.com)、
        网易考拉(goods.kaola.com)、当当网(product.dangdang.com)、亚马逊中国(www.amazon.cn)、国美(item.gome.com.cn)等电商
        商品详情的历史价格查询。

        :param url: 商品链接
        :return:
        """
        self.headers['X-Requested-With'] = "XMLHttpRequest"
        paramer = {
            "checkCode": "ccd99af476ce8db82fc8d65f2464fa55",
            "con": url
        }
        url = "http://detail.tmallvvv.com/dm/ptinfo.php"
        response = requests.post(url=url, data=paramer, headers=self.headers)  # 获取code标识
        g = json.loads(response.text)
        code = g['code']
        url = "http://182.61.13.46/vv/dm/historynew.php?code=" + code
        response = requests.get(url=url, headers=self.headers)

        match_result = re.search("chart\(\"(.*?)\",", response.text)
        try:
            all = re.findall("\((\d{4},\d{1,2},\d{1,2})\),(\d{1,})", match_result.group(1))  # ('2019,1,21', '399')
        except Exception:
            return iter([1])
        for item in all:
            date = item[0]  # 时间
            price = item[1]  # 价格
            yield (date, price)

    def get_goods_info(self, url) -> Dict:
        """
        获取商品卖家画像
        :param url:商品链接
        :return:
        """
        self.headers['X-Requested-With'] = "XMLHttpRequest"
        paramer = {
            "checkCode": "ccd99af476ce8db82fc8d65f2464fa55",
            "con": url
        }
        url = "http://detail.tmallvvv.com/dm/ptinfo.php"
        response = requests.post(url=url, data=paramer, headers=self.headers)  # 获取code标识
        g = json.loads(response.text)
        url = g['taoInfoUrl']
        response = requests.get(url, headers=self.headers)

        result = response.text[11:-1]
        g = json.loads(result)
        data = g['data']
        title = data['item']["title"]
        images = data['item']['images']  # 商品图片链接列表
        baseinfo = data['props']['groupProps'][0]['基本信息']  # 商品基本信息
        seller = data['seller']['evaluates']  # 卖家信息
        seller_info = list()
        for item in seller:
            """level: "1"
            levelBackgroundColor: "#EEEEEE"
            levelText: "高"
            levelTextColor: "#999999"
            score: "4.8 "
            title: "宝贝描述"
            tmallLevelBackgroundColor: "#EEEEEE"
            tmallLevelTextColor: "#999999"
            type: "desc"""
            seller_info.append(item)
        return {"data": {
            "title": title,
            "baseinfo": baseinfo,
            "seller": seller_info,
            "images": images
        }
        }
