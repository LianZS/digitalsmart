import time
import requests
from concurrent.futures import ThreadPoolExecutor
from django.test import TestCase


# Create your tests here.
def test_music_api():
    """
    测试音乐搜索功能
    :return:
    """
    search = ['我愿意', '失恋阵线联', '失恋', '护花使者', '恋爱', '我愿意为你', 'Auld', 'home', 'sad', '梦', '梦醒', '梦醒的我', 'beacuse', 'love']
    for key in search:
        url = "http://127.0.0.1:8000/interface/api/getMusic?name={0}&type=netease".format(key)
        thread_pool = ThreadPoolExecutor(30)

        def fast(r_url):
            response = requests.get(url=r_url)
            print(response)

        thread_pool.submit(fast, url)


def test_get_goods_price_change_api():
    data = {
        'url': 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.5.5348199esjc1uu&id=587898547820&skuId=4142881705398&user_id=740958699&cat_id=2&is_b=1&rn=52317a8a89e1b25d96493eeac75310a3',
        'token': 'bGlhbnpvbmdzaGVuZw=='
    }
    url = "http://127.0.0.1:8000/interface/api/getGoodsPriceResult"
    thread_pool = ThreadPoolExecutor(30)

    for i in range(100):
        def fast():
            response = requests.post(url=url, data=data)
            print(response)

        thread_pool.submit(fast)


def test_identity_authentication_api():
    url = "http://127.0.0.1:8000/interface/api/validation?card=440514199804220817"
    thread_pool = ThreadPoolExecutor(100)

    for i in range(1000):
        def fast():
            response = requests.get(url=url)
            print(response)

        thread_pool.submit(fast)


def test_analyse_url_api():
    data = {
        'url': 'https://blog.csdn.net/hhtnan/article/details/76586693',
        'allowPos': 'a'
    }
    url = "http://127.0.0.1:8000/interface/api/analyse?"
    thread_pool = ThreadPoolExecutor(3)

    for i in range(10):
        def fast():
            response = requests.post(url=url, data=data)
            print(response)

        thread_pool.submit(fast)


test_analyse_url_api()
