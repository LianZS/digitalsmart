import json
import requests
import re
import datetime
import uuid
import base64
import heapq
from threading import Thread, Semaphore
from queue import Queue
from jieba import analyse
from django.core.cache import cache
from digitalsmart.settings import redis_cache
from typing import Dict, Iterator, ByteString, Set
from urllib.parse import urlencode, urlparse
from bs4 import BeautifulSoup
from pdfminer.pdfparser import PDFParser, PDFDocument

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

from pdfminer.converter import PDFPageAggregator

from pdfminer.layout import *

from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from datainterface.models import PDFFile
from digitalsmart.celeryconfig import app


class Person:
    __slots__ = ["idcard", "area", "phone", "bir", "lunar", "gender", "latlon"]

    def __init__(self, idcard: int, area: str, phone: str, bir: str, lunar: str, gender: str, latlon: tuple):
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
    instanceflag = False
    instance = None

    def __new__(cls, *args, **kwargs):
        if NetWorker.instance is None:
            NetWorker.instance = super().__new__(cls)
        return NetWorker.instance

    def __init__(self):
        if not NetWorker.instanceflag:
            NetWorker.instanceflag = True

    def get_scence_distribution_data(self, pid, ddate, ttime) -> Dict:
        headers = dict()
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        headers['Host'] = 'heat.qq.com'
        paramer = {
            'region_id': pid,
            'datetime': "".join([str(ddate), ' ', str(ttime)]),
            'sub_domain': ''
        }

        url = "https://heat.qq.com/api/getHeatDataByTime.php?" + urlencode(paramer)

        try:
            response = requests.get(url=url, headers=headers)
        except requests.exceptions.ConnectionError:
            return {}
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            return {}

    def get_idcard_info(self, idcard):
        """
         身份证认证
        :param idcard:
        :return: {'身份证号码': '440514199804220817'}, {'发证地区': '广东省  汕头市 潮南区'}, {'电话区号': '0754'},
        {'出生日期': '1998年04月22日'}, {'农历': '一九九八年三月廿六'}, {'性别/生肖': '男 (21岁)  属虎'},
        {'当地经纬度': '23.366860,116.542328'}
        """
        headers = dict()
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        href = 'http://www.gpsspg.com/sfz/?q=' + str(idcard)
        response = requests.get(url=href, headers=headers)
        if response.status_code != 200:
            return Person(idcard, '', '', '', '', '', ())
        soup = BeautifulSoup(response.text, 'lxml')
        info = soup.find_all(name='tr')
        data = list()
        for item in info:
            flag = 0
            key = None
            for itemdic in item.find_all(name='td'):
                if flag == 0:
                    key = itemdic.string
                    if not key:
                        break
                if flag == 1:
                    value = itemdic.string
                    if not value:
                        return Person(idcard, '', '', '', '', '', ())
                    flag = 0

                    data.append({key: value})
                    key = None
                    continue

                flag += 1
        idcard = area = phone = lunar = bir = gender = latlon = None
        for i in range(len(data)):
            if i == 0:
                try:
                    idcard = int(data[i].get("身份证号码"))  # 假身份证
                except ValueError:
                    return Person(idcard, '', '', '', '', '', ())

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

    @app.task(queue="distribution", bind=True)
    def get_music_list(self, name, soft_type='netease', page=1):
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
        headers = dict()
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        url = "http://music.wandhi.com/"

        paramer = {
            "input": name,
            "filter": 'name',
            'type': soft_type,
            'page': page,

        }
        response = requests.post(url=url, data=paramer, headers=headers)
        data = list()
        if response.status_code != 200:
            data.append({"author": '', "url": '', "title": '', "lrc": '', "img": ''})
        else:
            g = json.loads(response.text)
            music_list = g['data']

            for item in music_list:
                author = item['author']
                url = item['url']  # 对url进行加密
                # 字符串 -> 二进制 -> base64编码
                url = base64.b64encode(url.encode())
                title = item['title']
                imgurl = item['pic']
                song_word = item['lrc']
                data.append({"author": author, "url": url.decode(), "title": title, "lrc": song_word, "img": imgurl})
                # yield {"author": author, "url": url.decode(), "title": title, "lrc": song_word, "img": imgurl}
        redis_key = "{soft_type}:{name}:{page}".format(soft_type=soft_type, name=name, page=page)  # 原型缓存key
        redis_cache.set(redis_key, value=str(data))
        redis_cache.expire(name=redis_key, time_interval=datetime.timedelta(minutes=5))

    def down_music_content(self, url) -> Iterator[ByteString]:
        """
        下载音乐
        :param url:下载音乐链接
        :return:
        """
        response = requests.get(url=url, stream=True)
        for fragment in response.iter_content(chunk_size=1024):
            yield fragment

    @app.task(queue="distribution", bind=True)
    def get_goods_price_change(self, url):
        """
        获取某商品的价格变化情况
        支持天猫(detail.tmall.com、detail.m.tmall.com)、淘宝(item.taobao.com、h5.m.taobao.com)、
        京东(item.jd.com、item.m.jd.com)、一号店(item.yhd.com）、苏宁易购(product.suning.com)、
        网易考拉(goods.kaola.com)、当当网(product.dangdang.com)、亚马逊中国(www.amazon.cn)、国美(item.gome.com.cn)等电商
        商品详情的历史价格查询。

        :param url: 商品链接
        :return:
        """
        data = list()  # 缓存数据容器
        headers = dict()
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        headers['X-Requested-With'] = "XMLHttpRequest"
        paramer = {
            "checkCode": "ccd99af476ce8db8746203d0ce47781b",  # 需要每天换一次

            "con": url
        }
        url = "http://detail.tmallvvv.com/dm/ptinfo.php"
        response = requests.post(url=url, data=paramer, headers=headers)  # 获取code标识
        if response.status_code != 200:
            return ('', 0)
        response.encoding = "utf-8"
        try:
            g = json.loads(response.text)
        except Exception:
            return ("", 0)
        code = g['code']
        url = "http://182.61.13.46/vv/dm/historynew.php?code=" + code
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            return ('', 0)
        else:
            match_result = re.search("chart\(\"(.*?)\",", response.text)
            try:
                all = re.findall("\((\d{4},\d{1,2},\d{1,2})\),(\d{1,})", match_result.group(1))  # ('2019,1,21', '399')
            except AttributeError:
                all = []

            for item in all:
                date = item[0]  # 时间
                price = item[1]  # 价格
                data.append((date, price))
            # 缓存
            redis_key = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
            redis_cache.set(name=redis_key, value=str(data))
            redis_cache.expire(name=redis_key, time_interval=datetime.timedelta(minutes=5))

    def get_goods_info(self, url) -> Dict:
        """
        获取商品卖家画像
        :param url:商品链接
        :return:
        """
        headers = dict()
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        headers['X-Requested-With'] = "XMLHttpRequest"
        paramer = {
            "checkCode": "ccd99af476ce8db82fc8d65f2464fa55",
            "con": url
        }
        url = "http://detail.tmallvvv.com/dm/ptinfo.php"
        response = requests.post(url=url, data=paramer, headers=headers)  # 获取code标识
        if response.status_code != 200:
            return {"data": {
                "title": '',
                "baseinfo": '',
                "seller": '',
                "images": ''
            }
            }
        g = json.loads(response.text)
        url = g['taoInfoUrl']
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"data": {
                "title": '',
                "baseinfo": '',
                "seller": '',
                "images": ''
            }
            }

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

    @app.task(queue="distribution", bind=True)
    def parse(self, filepath, uid, page_type, exchange_type, page):
        """

        将pdf转为doc格式

       :param filepath: 上传魏文件路径
       :param uid: 用户访问唯一标识
       :param page_type:  every---转换每一页;singular--转换奇数页;even--转换偶数页;specified--指定页转换,若为此选项，需要分析要转换哪些页，页码或者用逗号分隔的页码范围（例如：1,3-5，8,9表示要转换1,
        3,4,5,8,9）
       :param exchange_type: 转换类型有:  docx,doc
       :param page:  如1,3-5，8,9表示要转换1,3,4,5,8,9这几页
       :return:
       """

        # 存放需要指定解析的页码
        page_list = list()
        # 用来判断是用户想要哪种页面转换类型，1表示转换所有页，2表示偶数，3偶数页，4表示特定页码

        judge_pagetype = 0
        if page_type == "every":
            judge_pagetype = 1
        if page_type == "even":
            judge_pagetype = 2
        if page_type == "singular":
            judge_pagetype = 3

        if page_type == "specified":
            judge_pagetype = 4
            page_set = page.split(",")
            for page in page_set:
                try:
                    # 不是数字类型的话说明可能是3-8这类类型的
                    page = int(page)
                    page_list.append(page)
                except ValueError:
                    # "3-5类型的页面范围"
                    page_range = page.split("-")
                    if len(page_range) == 2:
                        try:
                            start_page = int(page_range[0])
                            end_page = int(page_range[1])
                            # 都是数字的情况下继续
                            # 起始必须小于等于结束页
                            if start_page <= end_page:
                                for page in range(start_page, end_page + 1):  # 右闭
                                    page = int(page)

                                    page_list.append(page)
                        except ValueError:
                            judge_pagetype = 1
        # 准备写入文件
        writepath = "./media/pdf/" + str(uid) + "." + exchange_type
        f = open(writepath, "a+")
        # fp = open(filepath, 'rb')  # 以二进制读模式打开

        # 用文件对象来创建一个pdf文档分析器
        fp = open(filepath, "rb")

        parser = PDFParser(fp)

        # 创建一个PDF文档

        doc = PDFDocument()

        # 连接分析器 与文档对象

        parser.set_document(doc)

        doc.set_parser(parser)

        # 提供初始化密码

        # 如果没有密码 就创建一个空的字符串

        doc.initialize()

        # 检测文档是否提供txt转换，不提供就忽略

        if not doc.is_extractable:

            raise PDFTextExtractionNotAllowed

        else:

            # 创建PDf 资源管理器 来管理共享资源

            rsrcmgr = PDFResourceManager()

            # 创建一个PDF设备对象

            laparams = LAParams()

            device = PDFPageAggregator(rsrcmgr, laparams=laparams)

            # 创建一个PDF解释器对象

            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量

            # num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0

            # 循环遍历列表，每次处理一个page的内容
            count = 0  # 计算第几页
            # 线程锁--用来记录有多少线程开启，等待所有线程结束后在写入文件
            q = Queue()
            lock = Semaphore(1)
            # 用于并发时存放解析出来的layout，用优先队列来保证解析成功后写入文件时顺序不会乱
            layout_list = []
            for page in doc.get_pages():  # doc.get_pages() 获取page列表
                def fast(page_index, page_content):
                    #  page_index指第几页，page_content页面内容，

                    if judge_pagetype == 1:
                        pass
                    if judge_pagetype == 2:
                        if page_index % 2 != 0:
                            q.put(1)
                            return
                    if judge_pagetype == 3:
                        if page_index % 2 == 0:
                            q.put(1)

                            return
                    if judge_pagetype == 4:
                        if len(page_list) == 0:
                            q.put(1)

                            return
                        if page_index not in page_list:
                            q.put(1)

                            return
                        # 页面所在列表的索引
                        element_index = page_list.index(page_index)
                        # 将解析了的页面索引pop掉，从而在列表长度为0时可以自动break结束
                        page_list.pop(element_index)

                    # num_page += 1  # 页面增一
                    # 加锁保证数据正确
                    lock.acquire()
                    interpreter.process_page(page_content)
                    layout = device.get_result()
                    lock.release()
                    heapq.heappush(layout_list, (page_index, layout))  # 设置优先级,页码数作为优先级，越小越优先
                    q.put(1)

                count += 1  # 这个表示第几页，同时也可表示有多少线程
                # 接受该页面的LTPage对象
                Thread(target=fast, args=(count, page)).start()

            # 用来统计线程完成的个数
            num = 0

            while 1:
                q.get()
                num += 1
                if count == num:  # 线程都完成了
                    break
            #  同步写入文件
            while layout_list:
                # 根据页码数大小从小到大取出内容写入文件中
                layout_tuple = heapq.heappop(layout_list)
                for x in layout_tuple[1]:
                    # if isinstance(x, LTImage):  # 图片对象
                    #
                    #     num_image += 1
                    #
                    # if isinstance(x, LTCurve):  # 曲线对象
                    #
                    #     num_curve += 1
                    #
                    # if isinstance(x, LTFigure):  # figure对象
                    #
                    #     num_figure += 1
                    #
                    if isinstance(x, LTTextBoxHorizontal):  # 获取文本内容

                        # num_TextBoxHorizontal += 1  # 水平文本框对象增一

                        # 保存文本内容

                        results = x.get_text()

                        f.write(results + '\n')

        fp.close()
        # 保存到数据库
        pdf = PDFFile()
        pdf.id = uid
        pdf.file = "pdf/" + str(uid) + "." + exchange_type
        pdf.save()
        f.close()
        redis_cache.set(str(uid), 1)  # 将转化状态写入内存，用户再次请求相同文件时直接取文件，不用再转换一边
        redis_cache.expire(filepath, time_interval=datetime.timedelta(minutes=60))
        print("success")
        # print('对象数量：\n', '页面数：%s\n' % num_page, '图片数：%s\n' % num_image, '曲线数：%s\n' % num_curve, '水平文本框：%s\n'
        #
        #       % num_TextBoxHorizontal)

    def analyse_word(self, url, allowpos, uid):
        """
          这个接口已经独立成一个程序了，加在这里效率太低下了。

        提取中文文本关键词以及频率
        :param url:请求链接
        :param allowpos:词性
        :return:
        Ag 形语素
        a 形容词
        m 数词
        n 名词
        nr 人名
        ns 地名
        t 时间词
        v 动词
        z 状态词
        ......详细见文档
        """
        # 解析获取域名
        domain = urlparse(url)
        netloc = domain.netloc

        self.headers['Host'] = netloc
        self.headers['Cookie'] = 'SUB=LianZS;'  # 记住，微博后台只是验证SUB是否为空，只要让他不空就行
        response = requests.get(url=url, headers=self.headers)
        if response.status_code != 200:
            return None
        text = response.text
        # 解析获取该网页编码方式
        soup = BeautifulSoup(text, 'lxml')
        # 默认编码gbk
        charset = "utf-8"
        # 找出该链接所用的编码方式
        try:
            charset = soup.find(name="meta", attrs={"charset": True})
            # 编码方式
            charset = charset.attrs["charset"]
        except AttributeError as e:
            meta = soup.find(name="meta", attrs={"content": re.compile("charset")})
            # 带有charset的字符串
            try:
                content = meta.attrs['content']
                content_set = content.split(";")

                for word in content_set:
                    if "charset" in word.lower():
                        # 编码
                        charset = word.split("=")[1]
            except AttributeError:
                charset = "utf-8"
            # 以;分割,分出带有charset的字符串段

        response.encoding = charset
        text = response.text
        # 保留中文文本
        text = re.sub("[^\u4E00-\u9FA5]", "", text)
        # 引入TextRank关键词抽取接口
        textrank = analyse.textrank
        # 基于TextRank算法进行关键词抽取
        keywords = textrank(sentence=text, allowPOS=(allowpos, allowpos, allowpos, allowpos), withWeight=True)
        cache.set(uid, keywords, 60 * 60)  # uid作为key，有效期60分钟
    # def get_baidu_doc(self, url, filetype):
    #     """
    #     解析下载链接
    #     :param url: 文档链接
    #     :param filetype: 文件类型，doc，ppt，pdf
    #     :return:
    #     """
    #     paramer = {
    #         "url": url,
    #         "type": filetype,
    #     }
    #     parase_url = "http://wenku.baiduvvv.com/ds.php?" + urlencode(paramer)
    #     response = requests.get(url=parase_url, headers=self.headers)  # 获取域名重要参数
    #     g = json.loads(response.text)
    #     domain = g['s']  # 域名
    #     f = g['f']
    #     h = g['h']
    #     paramer = {
    #         "url": url,
    #         "type": filetype,
    #         'f': f,
    #         'h': h,
    #         "sign": "1fb806c9fbd5b10c5fad7230a3f21ba5",
    #         "btype": "start",
    #         "callback": "callback2"
    #
    #     }
    #     url = domain + "/wkc.php?" + urlencode(paramer)  # 下载链接
    #     response = requests.get(url=url, headers=self.headers)
    #
    #     return {"url": url}
    #
    # def down_baidu_doc(self, url) -> Iterator[ByteString]:
    #     """
    #     下载百度文档
    #     :param url: 文档下载链接
    #     :return:
    #     """
    #     response = requests.get(url=url, stream=True, headers=self.headers)
    #     for fragment in response.iter_content(chunk_size=1024):
    #         yield fragment
