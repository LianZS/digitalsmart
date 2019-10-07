import re
import os
import sys
import datetime
import requests
import redis
import pickle
from typing import List, Iterator
from threading import Thread
from queue import Queue
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from jieba import analyse

sys.path[0] = os.path.abspath(os.curdir)
from datainterface.function.keyword_weight import KeyWordWeight

from digitalsmart.celeryconfig import app


class UrlDocAnalyse:
    """
    分析网页文本
    """
    doc_queue = Queue(1)  # 用来线程通信

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379)

    def analyse_word(self, target_url, pos, redis_key: str):
        """
        提取中文文本关键词以及频率------在内存不够调用celery情况下使用的方案
        :param target_url: 需要解析的链接
        :param pos:词性
        :param redis_key:缓存key
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
        headers['Accept-Language'] = "zh-CN,zh;q=0.9,be;q=0.8"

        Thread(target=self.parse_url, args=(target_url,)).start()
        keyword_objs: Iterator[KeyWordWeight] = self.analyse_text(pos)
        kw_list = list()
        for kw in keyword_objs:
            kw_list.append(kw)
        self.redis.set(redis_key, pickle.dumps(kw_list))

        self.redis.expire(redis_key, datetime.timedelta(minutes=60))

    @app.task(queue="word", bind=True)
    def analyse_url_info(self, target_url: str, pos: str) -> List[KeyWordWeight]:
        """
        提取中文文本关键词以及频率------在内存够调用celery情况下使用的方案
        :param target_url: 需要解析的链接
        :param pos:词性
        :return:
        """
        Thread(target=UrlDocAnalyse.parse_url, args=(target_url,)).start()
        keywords_objs: Iterator[KeyWordWeight] = UrlDocAnalyse.analyse_text(pos)
        return list(keywords_objs)

    @staticmethod
    def parse_url(target_url: str):
        """
        提取链接里面的中文文本
        :param target_url:
        :return:
        """
        # 解析获取域名
        domain = urlparse(target_url)
        netloc = domain.netloc
        headers = dict()
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        headers['Host'] = netloc
        headers['Cookie'] = 'SUB=LianZS;'  # 记住，微博后台只是验证SUB是否为空，只要让他不空就行
        response = None
        try:
            response = requests.get(url=target_url, headers=headers, timeout=5)
        except requests.exceptions.ReadTimeout:
            UrlDocAnalyse.doc_queue.put(None)

        if response.status_code != 200:
            return None
        content_type = response.headers['Content-Type']  # 网页Content-Type
        charset = None  # 编码格式
        try:
            charset = re.search("charset=(\S+)", content_type).group(1)  # 获取编码格式
        except AttributeError:
            # 默认编码gbk
            charset = "utf-8"
            # 若Response里找不到编码格式，则从网页里找
            text = response.text
            # 解析获取该网页编码方式
            soup = BeautifulSoup(text, 'lxml')

            # 找出该链接所用的编码方式
            try:
                charset = soup.find(name="meta", attrs={"charset": True})
                # 编码方式
                charset = charset.attrs["charset"]
            except AttributeError:
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

        UrlDocAnalyse.doc_queue.put(zh_text)

    @staticmethod
    def analyse_text(allowpos) -> Iterator[KeyWordWeight]:
        """
        提取关键词
        :param allowpos:
        :return:
        """
        rank = analyse.textrank
        # 基于TextRank算法进行关键词抽取
        text: list = UrlDocAnalyse.doc_queue.get()
        keywords = rank(sentence=text, topK=10, allowPOS=(allowpos, allowpos, allowpos, allowpos),
                        withWeight=True)
        for word, weight in keywords:
            yield KeyWordWeight(word, weight)


if __name__ == "__main__":

    try:
        obj = UrlDocAnalyse()
        url, allowPos, uid = sys.argv[1:4]
        obj.analyse_word(url, allowPos, uid)

    except Exception as e:
        print(sys.argv)
