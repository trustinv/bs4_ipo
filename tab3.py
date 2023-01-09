# -*- coding: utf-8 -*-

from datetime import timedelta
from datetime import datetime
from unittest import result
from urllib import response
from bs4 import BeautifulSoup
import sys, os
import requests
import json
import random
import pymysql
import time


def getRandomUserAgent():
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
        "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
    ]
    return user_agents[random.randint(0, len(user_agents) - 1)]


headers = {"User-Agent": getRandomUserAgent()}
# now = datetime.today() + timedelta(days= -5)
# today = (datetime.today() + timedelta(days= -5)).strftime("%Y/%m/%d")
# curr_date = (datetime.today() + timedelta(days= -5)).strftime("%Y-%m-%d %H:%M:%S")
now = datetime.today()
today = datetime.today().strftime("%Y/%m/%d")
curr_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
nowY = int(now.strftime("%Y"))
nowM = int(now.strftime("%m"))
nowd = int(now.strftime("%d"))
diffStart = datetime(nowY, nowM, nowd, 9, 0, 0)
diffEnd = datetime(nowY, nowM, nowd, 16, 0, 0)


# request 통신 에러 발생시 시스템 종료
try:
    req_url = "http://www.ipostock.co.kr/view_pg/view_03.asp?code=B202206162&gmenu="
    req = requests.get(req_url, headers=headers, json={"Content-Type": "application/json"})


except Exception as e:
    sys.exit()

soup = BeautifulSoup(req.content, "html.parser", from_encoding="utf-8")

table = soup.select_one("table.view_tb")
trs = table.select("tr")

a, b, c, d = [], [], [], []
extra = []
for idx, tr in enumerate(trs):
    tds = tr.select("td")
    # print(idx)
    # print("*" * 100)
    length = len(tds)
    for jdx, td in enumerate(tds):
        if idx == 1:
            extra.append(td.text)
        else:
            print(td.text)
            # a.append(td.text)
            # b.append(td.text)
            # c.append(td.text)
            # d.append(td.text)
    # print()
# print(a)
# print(b)
# print(c)
# print(d)
