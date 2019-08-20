from django.test import TestCase

# Create your tests here.
import requests
import csv
import time
from selenium import webdriver

post_url = "http://scenicmonitor.top/attractions/admin/uploadComment"

f = open("/Volumes/Tigo/finished/深圳欢乐谷/评价.csv", 'r', encoding="gbk")
read = csv.reader(f)
read.__next__()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
}
drive = webdriver.Chrome()
drive.get(
    'http://127.0.0.1:8020/DigitalSmart/manager/scencedata.html?area=%E6%B7%B1%E5%9C%B3%E6%AC%A2%E4%B9%90%E8%B0%B7&pid=6')
count = 2
for item in read:
    drive.find_element_by_id('add-comment-tr').click()

    username = item[0]
    commment = item[1]

    month, day, year = item[2].split('/', maxsplit=3)
    date = "{0}-{1}-{2}".format(year, month, day)
    commmentlike = int(item[3])

    element_xpath = "//td[@id='{0}']".format('user-' + str(count))
    username_element = drive.find_element_by_xpath(element_xpath)  # 用户节点
    username_element.send_keys(username)
    commment_element = drive.find_element_by_xpath(element_xpath + "/../td[2]")  # 评论节点
    commment_element.send_keys(commment)
    commmentlike_element = drive.find_element_by_xpath(element_xpath + "/../td[3]")  # 评分节点
    commmentlike_element.send_keys(commmentlike)
    date_element = drive.find_element_by_xpath(element_xpath + "/../td[4]")  # 时间节点
    date_element.send_keys(date)


    count += 1

drive.find_element_by_id('send2').click()
drive.close()