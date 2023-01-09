import sys
import requests
import re

from bs4 import BeautifulSoup
from agents import get_user_agents


def extract_data_from_table1(soup):
    result = []
    table = soup.find("table", width="780", cellpadding="0", class_="view_tb")
    trs = table.select("tr")[2:-1]
    for tr in trs:
        tds = tr.select("td")
        temp = []
        for td in tds:
            temp.append(td.text)
        result.append(temp)
    return result


def extract_data_from_table2(soup):
    result = []
    table = soup.find_all("table", width="780", cellspacing="1", class_="view_tb2")[-1]
    trs = table.select("tr")
    for tr in trs:
        tds = tr.select("td")
        for idx, td in enumerate(tds, 1):
            if idx % 2 == 0:
                result.append(td.text.strip())
    return result

    # return [td.text for td in tds]


def scrape_ipostock(url):
    headers = {"User-Agent": get_user_agents()}

    # request 통신 에러 발생시 시스템 종료
    try:
        req = requests.get(url, headers=headers)
    except Exception:
        sys.exit()

    soup = BeautifulSoup(req.content, "html.parser", from_encoding="utf-8")

    table1_data = extract_data_from_table1(soup)
    table2_data = extract_data_from_table2(soup)
    return table1_data + table2_data


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_05.asp?code=B202206162&gmenu="
    result = scrape_ipostock(url)
    print(result)
