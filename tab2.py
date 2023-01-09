import sys
import requests
import re
from pprint import pprint as pp

from bs4 import BeautifulSoup
from agents import get_user_agents


def extract_data_from_table1(table):
    result = []
    tds = table.select("td")
    pattern = r"\d+[,.]\d+|\d+"

    raw_data = tds[-3:]

    for item in raw_data:
        text_data = item.text
        match = re.search(pattern, text_data)
        if match:
            result.append(match.group())
    return result


def extract_data_from_table2(table):
    result = []
    tds = table.select("td")
    pattern = r"\d+[,.]\d+|\d+"

    raw_data = tds[-3:]

    for item in raw_data:
        text_data = item.text
        match = re.search(pattern, text_data)
        if match:
            result.append(match.group())

    print(result)
    return result

def extract_data_from_table3(table):
    result = {"보호예수": [], "유통가능": []}
    trs = table.select("tr")[2:-2]
    for idx_tds, tds in enumerate(trs):
        if idx_tds % 2 == 0:
            data_type = "보호예수"
        else:
            data_type = "유통가능"
        data = []
        for idx_td, td in enumerate(tds):
            if idx_td % 2 == 1:
                data.append(td.text)
        result[data_type].append(data)

    result["보호예수"][0].pop(0)
    return result

def scrape_ipostock(url):
    headers = {"User-Agent": get_user_agents()}

    try:
        req = requests.get(url, headers=headers)
    except Exception:
        sys.exit()

    soup = BeautifulSoup(req.content, "html.parser", from_encoding="utf-8")
    table1, table2, table3 = soup.find_all("table", class_="view_tb")[:-1]

    table1_data = extract_data_from_table1(table1)
    table2_data = extract_data_from_table2(table2)
    table3_data = extract_data_from_table3(table3)

    return table1_data + table2_data, table3_data


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_02.asp?code=B202206162&gmenu="
    result = scrape_ipostock(url)
    print(result)
