# -*- coding: utf-8 -*-
import sys
import requests
import re

from bs4 import BeautifulSoup
from agents import get_user_agents


def extract_data_from_table1(table):
    tds = table.find_all("td", attrs={"height": re.compile(r"^[27-9]\d*$")})
    return [td.text for td in tds]


def extract_data_from_table2(talbe):
    result = []
    for idx, tr in enumerate(talbe, 1):
        if idx % 2 == 0:
            tds = tr.select("td")
            for jdx, td in enumerate(tds):
                if jdx % 2 == 1:
                    result.append(td.text)
    return result


def extract_data_from_table3(table):
    result = []
    trs = table.select("tr")[1:]
    for tr in trs:
        tds = tr.select("td")
        temp = []
        for td in tds:
            if re.search(r"\d+[,\d+]*", td.text):
                temp.append(td.text)
        result.append(temp)
    return result


def extract_data_from_table4(table):
    result = []
    trs = table.select("tr")[1:]
    for tr in trs:
        tds = tr.select("td")
        temp = []
        for td in tds:
            data = td.text
            temp.append(data)
        result.append(temp)
    return result


def scrape_ipostock(url):
    headers = {"User-Agent": get_user_agents()}

    # request 통신 에러 발생시 시스템 종료
    try:
        req = requests.get(url, headers=headers)
    except Exception:
        sys.exit()

    soup = BeautifulSoup(req.content, "html.parser", from_encoding="utf-8")
    table1, table2, table3, table4, _ = soup.select("table.view_tb")

    table1_data = extract_data_from_table1(table1)
    table2_data = extract_data_from_table2(table2)
    table3_data = extract_data_from_table3(table3)
    table4_data = extract_data_from_table4(table4)
    return table1_data + table2_data + table3_data + table4_data


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_04.asp?code=B202206162&gmenu="
    result = scrape_ipostock(url)
    print(result)
