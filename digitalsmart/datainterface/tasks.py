import json
import requests
from urllib.parse import urlencode
from digitalsmart.celeryconfig import app


class NetWorker(object):
    def __init__(self):
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
