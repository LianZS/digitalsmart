from django.test import TestCase

# Create your tests here.
import csv
import time
import random
import os
import pymysql
import json
import requests
from threading import Thread
from selenium import webdriver


class WebDriver(TestCase):
    def __init__(self):
        self.drive = webdriver.Chrome()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drive.close()

    def send_comment(self, url, filepath):
        f = open(filepath, 'r', encoding="gbk")
        read = csv.reader(f)
        read.__next__()

        self.drive.get(url)

        count = 1

        for item in read:

            self.drive.find_element_by_id('add-comment-tr').click()

            username = item[0]
            commment = item[1]
            try:
                month, day, year = item[2].split('/', maxsplit=3)
                date = "{0}-{1}-{2}".format(year, month, day)

            except ValueError:
                date = item[2]
            commmentlike = int(item[3])
            if commmentlike == 0:
                commmentlike = random.randint(1, 5)
            element_xpath = "//td[@id='{0}']".format('user-' + str(count))
            try:
                username_element = self.drive.find_element_by_xpath(element_xpath)  # 用户节点
            except Exception:  # 因为速度太快导致节点还没生成
                self.drive.find_element_by_id('add-comment-tr').click()

                time.sleep(1)
                username_element = self.drive.find_element_by_xpath(element_xpath)  # 用户节点

            username_element.send_keys(username)
            commment_element = self.drive.find_element_by_xpath(element_xpath + "/../td[2]")  # 评论节点
            commment_element.send_keys(commment)
            commmentlike_element = self.drive.find_element_by_xpath(element_xpath + "/../td[3]")  # 评分节点
            commmentlike_element.send_keys(commmentlike)
            date_element = self.drive.find_element_by_xpath(element_xpath + "/../td[4]")  # 时间节点
            date_element.send_keys(date)

            count += 1

        self.drive.find_element_by_id('send2').click()

    def load_html(self, url):
        self.drive.get(url)

    def send_pic(self, filepath):
        elemetn_xpath = "//div[@class='{0}']".format("card-panel")
        self.drive.find_element_by_xpath(elemetn_xpath + "/li[1]").click()

        self.drive.find_element_by_id("fileinp").send_keys(filepath)
        self.drive.find_element_by_id("btn").click()
        time.sleep(4)


def send_comment_data():  # 传到了商丘古文化旅游区
    db = pymysql.connect(host='localhost', user="root", password="lzs87724158",
                         database="digitalsmart", port=3306)
    cur = db.cursor()
    sql = "select area,pid from digitalsmart.scencemanager where flag=0"
    cur.execute(sql)
    result = cur.fetchall()
    web = WebDriver()
    rootpath = "/Volumes/Tigo/易班项目数据/评论/"
    area_map = dict()
    for item in result:
        area = item[0]
        pid = item[1]
        area_map[area] = pid
    for filedir in os.listdir(rootpath):

        try:
            pid = area_map[filedir]
        except KeyError:
            continue
        response = requests.get(url="http://scenicmonitor.top/attractions/api/getComment?&pid={0}".format(pid))
        g = json.loads(response.text)
        if len(g["comment"]) > 0:
            continue
        for file in os.listdir(rootpath + filedir):
            file_type = file.split(".")[1]
            if file_type == "csv":
                filepath = rootpath + filedir + "/" + file
                url = "http://127.0.0.1:8020/DigitalSmart/manager/scencedata.html?area={0}&pid={1}".format(filedir, pid)
                try:
                    web.send_comment(url=url, filepath=filepath)
                    print("send:{0}".format(filedir))

                except Exception:
                    print("error:{0}".format(filedir))
            time.sleep(3)


def send_scence_pic():
    db = pymysql.connect(host='localhost', user="root", password="lzs87724158",
                         database="digitalsmart", port=3306)
    cur = db.cursor()
    sql = "select area,pid from digitalsmart.scencemanager where flag=0 "
    cur.execute(sql)
    result = cur.fetchall()
    web = WebDriver()
    rootpath = "/Volumes/Tigo/易班项目数据/景区/景区/"

    area_map = dict()
    for item in result:
        area = item[0]
        pid = item[1]
        area_map[area] = pid
    flag = 0
    for filedir in os.listdir(rootpath):
        if filedir == "北京市颐和园":
            flag = 1
            continue
        if flag != 1:
            continue
        key = get_pid(area_map, filedir)
        if key is not None:
            pid = area_map[key]
            url = "http://127.0.0.1:8020/DigitalSmart/manager/scencedata.html?area={0}&pid={1}".format(filedir,
                                                                                                       pid)
            web.load_html(url=url)

            for file in os.listdir(rootpath + filedir):
                file_type = file.split(".")[1]

                if file_type == "png" or file_type == "jpg" or file_type == "jpeg":
                    filepath = rootpath + filedir + "/" + file
                    try:
                        web.send_pic(filepath)

                        print("send:{0}".format(filedir))

                    except Exception:
                        print("error:{0}".format(filedir))
            time.sleep(8)

def get_pid(map, longkey):
    for key in map.keys():
        if key in longkey:
            return key
    else:
        return None


if __name__ == "__main__":  # send:吉安市井冈山风景名胜区
    send_scence_pic()
    # Thread(target=send_scence_pic, args=()).start()
    # send_comment_data()
