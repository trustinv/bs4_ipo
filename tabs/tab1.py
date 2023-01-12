import sys
import requests

from bs4 import BeautifulSoup
from agents import get_user_agents
from collections import ChainMap


def extract_data_from_table1(table):
    keys = [
        "ci_market_separation",
        "ci_name",
        "ci_code",
    ]
    result = []
    trs = table.select("tr")
    for tds in trs:
        for idx, td in enumerate(tds):
            name = td.text
            img_tag = td.find("img")
            if img_tag is not None and img_tag != -1:
                img_tag = img_tag["src"]
                name, code = name.strip().split("\n")
                result.extend((img_tag, name, code))
    return dict(zip(keys, result))


def extract_data_from_table2(table):
    keys = [
        "ci_ceo",
        "ci_establishment_date",
        "ci_company_separation",
        "ci_brn",
        "ci_tel",
        "ci_homepage",
        "ci_settlement_month",
        "ci_worker_cnt",
        "ci_industries",
        "ci_important_product",
        "ci_stocks_separation",
        "ci_lead_manager",
        "ci_address",
    ]

    result = []
    trs = table.select("tr")
    for idx_tr, tr in enumerate(trs):
        tds = tr.select("td.txt")
        result.extend(td.text if td.text is not None else "" for td in tds)
    return dict(zip(keys, result))


def extract_data_from_table3(table):
    keys = [
        "ci_review_c_date",
        "ci_review_a_date",
        "ci_turnover",
        "ci_before_corporate_tax",
        "ci_net_profit",
        "ci_capital",
        "ci_largest_shareholder",
        "ci_largest_shareholder_rate",
        "ci_po_expected_price",
        "ci_public_offering_stocks",
        "ci_po_expected_amount",
        "ci_listing_expected_stocks",
    ]
    tds = table.select('tr > td[width="240"]')
    result = [td.text if td.text is not None else "" for td in tds]
    return dict(zip(keys, result))


def scrape_ipostock(code):
    headers = {"User-Agent": get_user_agents()}
    url = f"http://www.ipostock.co.kr/view_pg/view_01.asp?code={code}"
    # request 통신 에러 발생시 시스템 종료
    try:
        req = requests.get(url, headers=headers)
    except Exception:
        sys.exit()

    soup = BeautifulSoup(req.content, "lxml", from_encoding="utf-8")
    table1 = soup.find("table", width="550", style="margin:0 auto;")
    table2, table3 = soup.select('table[width="780"][class="view_tb"]')

    result = {
        **extract_data_from_table1(table1),
        **extract_data_from_table2(table2),
        **extract_data_from_table3(table3),
    }
    return result


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_01.asp?code=B202206162&gmenu="
    result = scrape_ipostock(url)
    from schemas.general import GeneralCreateSchema

    g = GeneralCreateSchema(**result)
    from pprint import pprint as pp

    pp(g)
