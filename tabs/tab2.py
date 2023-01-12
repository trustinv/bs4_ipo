import sys
import requests
import re
from pprint import pprint as pp

from bs4 import BeautifulSoup
from agents import get_user_agents


def extract_data_from_table1(table):
    keys = [
        "ci_before_po_capital",
        "ci_before_po_stocks",
    ]
    temp = []
    tds = table.select("td")
    pattern = r"\d+[,.]\d+|\d+"

    raw_data = tds[-3:]

    for item in raw_data:
        text_data = item.text
        match = re.search(pattern, text_data)
        if match:
            temp.append(match.group())
    result = dict(zip(keys, temp))
    return result


def extract_data_from_table2(table):
    keys = [
        "ci_after_po_capital",
        "ci_after_po_stocks",
    ]
    temp = []
    tds = table.select("td")
    pattern = r"\d+[,.]\d+|\d+"

    raw_data = tds[-3:]

    for item in raw_data:
        text_data = item.text
        match = re.search(pattern, text_data)
        if match:
            temp.append(match.group())
    result = dict(zip(keys, temp))
    return result


def extract_data_from_table3(table, url):
    keys = [
        "ci_category",
        "ci_category_name",
        "ci_normal_stocks",
        "ci_first_stocks",
        "ci_share_rate",
        "ci_protection_date",
    ]
    tds = table.select('tr[height="23"] > td')
    flag = 1
    result = []
    categories1 = []
    categories2 = []

    for idx, i in enumerate(tds[1:]):
        if flag == 1:
            if "유통가능" in i.text:
                flag = 2
                continue
            categories1.append(i.text)
        else:
            categories2.append(i.text)

    def nesten_list(temp):
        return list(map(list, zip(*[iter(temp)] * 5)))

    temp3 = nesten_list(categories1)
    temp4 = nesten_list(categories2)
    for i in temp3:
        i.insert(0, 1)
    for j in temp4:
        j.insert(0, 2)
    result = [dict(zip(keys, lst)) for lst in temp3 + temp4]
    return result


def scrape_ipostock(code):
    url = f"http://www.ipostock.co.kr/view_pg/view_02.asp?code={code}"
    headers = {"User-Agent": get_user_agents()}

    # try:
    req = requests.get(url, headers=headers)

    soup = BeautifulSoup(req.content, "lxml", from_encoding="utf-8")
    table1, table2, table3 = soup.find_all("table", class_="view_tb")[:3]

    table1_data = extract_data_from_table1(table1)
    table2_data = extract_data_from_table2(table2)
    table3_data = extract_data_from_table3(table3, url)

    return {**table1_data, **table2_data}, table3_data
    # except Exception:
    #     print(url)
    #     sys.exit()


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_02.asp?code=B202206162&gmenu="
    general_result, shareholder_results = scrape_ipostock(url)
    from schemas.general import GeneralCreateSchema
    from schemas.shareholder import ShareholderCreateSchema

    # pp(shareholder_result)
    g = GeneralCreateSchema(**general_result)
    s = [ShareholderCreateSchema(**shareholder) for shareholder in shareholder_results]

    pp(s)
