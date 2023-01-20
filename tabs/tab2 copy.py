import time
import requests
from pprint import pprint as pp

from bs4 import BeautifulSoup


def get_capital_n_stcks(table):
    capital = table.select_one('td[width="*"]').get_text().split("억원")[0].strip()
    stocks = (
        table.select_one("tr:nth-of-type(2) td:nth-of-type(2)")
        .get_text()
        .strip()
        .split("주")[0]
        .strip()
        .replace(",", "")
    )
    return capital, stocks


def extract_data_from_table1(table):
    capital, stocks = get_capital_n_stcks(table)
    return dict(ci_before_po_capital=capital, ci_before_po_stocks=stocks)


def extract_data_from_table2(table):
    capital, stocks = get_capital_n_stcks(table)
    return dict(ci_after_po_capital=capital, ci_after_po_stocks=stocks)


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

    session = requests.Session()
    session.timeout = 3
    while True:
        try:
            req = session.get(url)
            req.encoding = "utf-8"
            print(req.text)
            # req = requests.get(url)
            soup = BeautifulSoup(req.content, "lxml")
            break
        except requests.exceptions.ReadTimeoutError as e:
            print("Request failed, retrying in 5 seconds...")
            print(e)
            time.sleep(0.3)
        except requests.exceptions.ConnectionError as e:
            print("Request failed, retrying in 5 seconds...")
            print(e)
            time.sleep(0.3)
        except requests.exceptions.RequestException as e:
            print("Request failed, retrying in 5 seconds...")
            print(e)
    table1, table2, table3 = soup.find_all("table", class_="view_tb")[:3]

    table1_data = extract_data_from_table1(table1)
    table2_data = extract_data_from_table2(table2)
    table3_data = extract_data_from_table3(table3, url)

    return {**table1_data, **table2_data}, table3_data


if __name__ == "__main__":

    code = "B202010131"
    general_result, shareholder_results = scrape_ipostock(code)
    from schemas.general import GeneralCreateSchema
    from schemas.shareholder import ShareholderCreateSchema

    # pp(shareholder_result)
    pp(general_result)
    g = GeneralCreateSchema(**general_result)
    s = [ShareholderCreateSchema(**shareholder) for shareholder in shareholder_results]

    # print("*" * 100)
    # print(s, len(s))
    pp(s[0].dict())
    pp(s[1].dict())
    pp(s[2].dict())
    pp(s[3].dict())
    pp(s[4].dict())
    pp(s[5].dict())
    pp(s[6].dict())
