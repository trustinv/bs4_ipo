# -*- coding: utf-8 -*-
import sys
import requests
import re

from bs4 import BeautifulSoup
from agents import get_user_agents
from pprint import pprint as pp


def extract_data_from_table1(table):
    keys = [
        "ci_big_ir_plan",
        "ci_demand_forecast_date",
        "ci_public_subscription_date",
        "ci_refund_date",
        "ci_payment_date",
        "ci_listing_date",
    ]
    result = [td.text for td in table.find_all("td", attrs={"height": re.compile(r"^[27-9]\d*$")})]
    result = dict(zip(keys, result))
    return result


def extract_data_from_table2(talbe):
    keys = [
        "ci_hope_po_price",
        "ci_hope_po_amount",
        "ci_confirm_po_price",
        "ci_confirm_po_amount",
        "ci_subscription_warrant_money_rate",
        "ci_subscription_competition_rate",
    ]
    result = []
    for idx, tr in enumerate(talbe, 1):
        if idx % 2 == 0:
            tds = tr.select("td")
            for jdx, td in enumerate(tds):
                if jdx % 2 == 1:
                    result.append(td.text)
    result = dict(zip(keys, result))
    return result


def extract_data_from_table3(table):
    keys = [
        "ci_professional_investor_stock",
        "ci_professional_investor_rate",
        "ci_esa_stock",
        "ci_esa_rate",
        "ci_general_subscriber_stock",
        "ci_general_subscriber_rate",
        "ci_overseas_investor_stock",
        "ci_overseas_investor_rate",
    ]
    result = []
    trs = table.select("tr")[1:]
    for tr in trs:
        tds = tr.select("td")
        for td in tds:
            if re.search(r"\d+[,\d+]*", td.text):
                result.append(td.text)
    result = {key: value for key, value in zip(keys, result)}
    return result


def extract_data_from_table4(table):
    keys = [
        "ci_stock_firm",
        "ci_assign_quantity",
        "ci_limit",
        "ci_note",
    ]
    td_datas = []
    trs = table.select("tr")[1:]
    for tr in trs:
        tds = tr.select("td")
        temp = []
        for td in tds:
            data = td.text
            temp.append(data)
        td_datas.append(temp)
    result = [dict(zip(keys, result)) for result in td_datas]
    return result


def scrape_ipostock(code):
    url = f"http://www.ipostock.co.kr/view_pg/view_04.asp?code={code}"
    headers = {"User-Agent": get_user_agents()}

    try:
        req = requests.get(url, headers=headers)
    except Exception:
        sys.exit()

    soup = BeautifulSoup(req.content, "lxml", from_encoding="utf-8")
    table1, table2, table3, table4, *_ = soup.select("table.view_tb")

    table1_data = extract_data_from_table1(table1)
    table2_data = extract_data_from_table2(table2)
    table3_data = extract_data_from_table3(table3)
    table4_data = extract_data_from_table4(table4)
    return {**table1_data, **table2_data, **table3_data}, table4_data


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_04.asp?code=B202206162&gmenu="
    general_result, subscriber_results = scrape_ipostock(url)
    from schemas.general import GeneralCreateSchema
    from schemas.subscriber import SubscriberCreateSchema

    g = GeneralCreateSchema(**general_result)
    s = [SubscriberCreateSchema(**subscriber_result) for subscriber_result in subscriber_results]

    from pprint import pprint as pp

    pp(g)
    pp(s)
