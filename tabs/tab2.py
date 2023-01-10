import sys
import requests
import re
from pprint import pprint as pp

from bs4 import BeautifulSoup
from agents import get_user_agents


def extract_data_from_table1(table):
    keys = {
        "ci_before_po_capital",
        "ci_before_po_stocks",
    }
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
    keys = {
        "ci_after_po_capital",
        "ci_after_po_stocks",
    }
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


def extract_data_from_table3(table):
    keys = [
        "ci_category",
        "ci_category_name",
        "ci_normal_stocks," "ci_first_stocks",
        "ci_share_rate",
        "ci_protection_date",
    ]
    temp1 = []
    temp2 = []
    trs = table.select('tr[height="23"]')  # [2:-2]
    boho_rowspan, utong_rowspan = [
        int(data["rowspan"]) for tr in trs if (data := tr.select_one("td[rowspan]")) is not None
    ]
    a = trs[: boho_rowspan - 1]
    b = trs[boho_rowspan - 1 :]
    tds = table.select('tr[height="23"] > td')
    # print(tds[0])
    # print(tds[1])
    # print(tds[2])
    # print(tds[3])
    flag = 1
    result = []
    temp1 = []
    temp2 = []
    for idx, i in enumerate(tds[1:]):
        if flag == 1:
            if "유통가능" in i.text:
                flag = 2
                continue
            print(idx, flag, i.text)
            temp1.append(i.text)
        else:
            print(idx, flag, i.text)
            temp2.append(i.text)

    def nesten_list(temp):
        return list(map(list, zip(*[iter(temp)] * 5)))

    temp3 = nesten_list(temp1)
    temp4 = nesten_list(temp2)


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

    # return table1_data + table2_data, table3_data


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_02.asp?code=B202206162&gmenu="
    result = scrape_ipostock(url)
    print(result)


k = [
    "\xa0\xa0[최대주주 등]",
    "\xa0\xa068,914,240 주",
    "0 주",
    "\xa0\xa066.29 %",
    "\xa0\xa0상장 후 6개월",
    "\xa0\xa0[기타주주]",
    "\xa0\xa019,712,848 주",
    "0 주",
    "\xa0\xa018.96 %",
    "\xa0\xa0상장 후 3개월",
    "\xa0\xa0[공모시 우리사주조합]",
    "\xa0\xa02,600,000 주",
    "0 주",
    "\xa0\xa02.50 %",
    "\xa0\xa0상장 후 1년",
]
d = list(map(list, zip(*[iter(k)] * 5)))
