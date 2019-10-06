from __future__ import absolute_import
import re
import sys
import datetime
import requests
import redis
from typing import List, Dict
from threading import Thread
from queue import Queue
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from jieba import analyse


# from digitalsmart.settings import redis_cache
# from digitalsmart.celeryconfig import app


class UrlDocAnalyse:
    """
    分析网页文本
    """

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379)
        self.doc_queue = Queue(1)  # 用来线程通信

    # @app.task(queue="word", bind=True)
    def analyse_word(self, url, allowpos, uid):
        """
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
        headers = dict()  # 网络爬虫请求头
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        q = Queue()

        def request():

            # 解析获取域名
            domain = urlparse(url)
            netloc = domain.netloc

            headers['Host'] = netloc
            headers['Cookie'] = 'SUB=LianZS;'  # 记住，微博后台只是验证SUB是否为空，只要让他不空就行
            response = requests.get(url=url, headers=headers, timeout=5)
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
                try:
                    content = meta.attrs['content']
                    content_set = content.split(";")

                    for word in content_set:
                        if "charset" in word.lower():
                            # 编码
                            charset = word.split("=")[1]
                except AttributeError:
                    charset = "gbk"
            response.encoding = charset
            text = response.text
            # 保留中文文本
            text = re.sub("[^\u4E00-\u9FA5]", "", text)
            q.put(text)

        def rank():
            # 引入TextRank关键词抽取接口
            textrank = analyse.textrank
            text: list = q.get()
            # 基于TextRank算法进行关键词抽取
            keywords = textrank(sentence=text, topK=10, allowPOS=(allowpos, allowpos, allowpos, allowpos),
                                withWeight=True)
            # 缓存
            self.redis.set(str(uid), str(keywords))
            self.redis.expire(str(uid), datetime.timedelta(minutes=60))
            return keywords

        Thread(target=request, args=()).start()
        rank()

    # @app.task(queue="word", bind=True)
    def analyse_url_info(self, target_url: str, allowpos: str) -> List[tuple]:
        """
        解析文本链接
        :param target_url:
        :param allowpos:
        :return:
        """
        Thread(target=self.parse_url, args=(target_url,)).start()
        keywords = self.analyse_text(allowpos)
        return keywords

    def parse_url(self, target_url: str):
        # 解析获取域名
        domain = urlparse(target_url)
        netloc = domain.netloc
        headers = dict()
        headers['Host'] = netloc
        headers['Cookie'] = 'SUB=LianZS;'  # 记住，微博后台只是验证SUB是否为空，只要让他不空就行
        response = requests.get(url=target_url, headers=headers, timeout=5)

        if response.status_code != 200:
            return None
        content_type = response.headers['Content-Type']  # 网页Content-Type
        charset = re.findall("charset=(.*?)", content_type)  # 获取编码格式

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
            try:
                content = meta.attrs['content']
                content_set = content.split(";")

                for word in content_set:
                    if "charset" in word.lower():
                        # 编码
                        charset = word.split("=")[1]
            except AttributeError:
                charset = "gbk"
        response.encoding = charset
        text = response.text
        # 保留中文文本
        zh_text = re.sub("[^\u4E00-\u9FA5]", "", text)

        self.doc_queue.put(zh_text)

    def analyse_text(self, allowpos) -> List[tuple]:

        textrank = analyse.textrank
        # 基于TextRank算法进行关键词抽取
        text: list = self.doc_queue.get()
        keywords = textrank(sentence=text, topK=10, allowPOS=(allowpos, allowpos, allowpos, allowpos),
                            withWeight=True)
        return keywords


if __name__ == "__main__":

    try:
        obj = UrlDocAnalyse()
        obj.analyse_url_info("https://www.cnblogs.com/bw13/p/6549248.html", 'n')
        # url, allowPos, uid = sys.argv[1:4]
        # obj.analyse_word(url, allowPos, uid)

    except Exception as e:
        print(sys.argv)
