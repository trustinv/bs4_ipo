import sys
import requests
import re

from bs4 import BeautifulSoup
from agents import get_user_agents


def extract_data_from_table1(soup):
    result = []
    table = soup.find("table", width="550", style="margin:0 auto;")
    trs = table.select("tr")
    for tds in trs:
        for idx, td in enumerate(tds):
            name = td.text
            img_tag = td.find("img")
            if img_tag is not None and img_tag != -1:
                img_tag = img_tag["src"]

                result.append(img_tag)
                result.append(name)
    return result


def extract_data_from_table2(table):
    result = []

    trs = table.select("tr")
    # print(trs)
    for idx_tr, tr in enumerate(trs):
        for idx_td, td in enumerate(tr):
            if idx_td == 3 or idx_td == 7 or idx_td == 9:
                result.append(td.text)
    return result


def extract_data_from_table3(table):
    result = []

    trs = table.select("tr")
    # print(trs)
    for idx_tr, tr in enumerate(trs):
        for idx_td, td in enumerate(tr):
            if idx_td == 3 or idx_td == 7 or idx_td == 9:
                result.append(td.text)
    return result


def scrape_ipostock(url):
    headers = {"User-Agent": get_user_agents()}

    # request 통신 에러 발생시 시스템 종료
    try:
        req = requests.get(url, headers=headers)
    except Exception:
        sys.exit()

    soup = BeautifulSoup(req.content, "html.parser", from_encoding="utf-8")

    table1_data = extract_data_from_table1(soup)
    table2, table3 = soup.find_all("table", width="780", class_="view_tb")
    table2_data = extract_data_from_table2(table2)
    table3_data = extract_data_from_table3(table3)

    return table1_data + table2_data + table3_data


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_01.asp?code=B202206162&gmenu="
    result = scrape_ipostock(url)
    print(result)
