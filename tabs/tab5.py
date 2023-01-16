import sys
import requests
import re

from bs4 import BeautifulSoup
from agents import get_user_agents


def extract_data_from_table1(soup, url):
    try:
        keys = [
            "ci_price",
            "ci_incidence",
            "ci_incidence_specific_gravity",
            "ci_participation",
            "ci_participation_specific_gravity",
        ]
        results = []
        table = soup.find("table", width="780", cellpadding="0", class_="view_tb")
        trs = table.select("tr")[2:-1]
        for tr in trs:
            tds = tr.select("td")
            temp = []
            for td in tds:
                temp.append(td.text)
            results.append(temp)

        result = [dict(zip(keys, result)) for result in results]

        return result
    except AttributeError:
        result = [
            {
                "ci_price": "",
                "ci_incidence": 0,
                "ci_incidence_specific_gravity": 0.0,
                "ci_participation": 0,
                "ci_participation_specific_gravity": 0.0,
            }
        ]
        return result


def extract_data_from_table2(soup, url):
    try:
        table = soup.find_all("table", width="780", cellspacing="1", class_="view_tb2")[-1]
        result = dict(
            ci_competition_rate=table.select_one(
                "tr:nth-of-type(1) > td:nth-of-type(2) > font > strong"
            )
            .get_text()
            .replace(" ", "")
            .replace("\xa0", ""),
            ci_promise_content=table.select_one("tr:nth-of-type(2) > td:nth-of-type(2)")
            .get_text()
            .strip(),
            ci_promise_rate=table.select_one("tr:nth-of-type(3) > td:nth-of-type(2)")
            .get_text()
            .strip(),
        )
        return result
    except AttributeError:
        # 해당 테이블이 존재하지 않을 경우 기본 값으로 데이터를 넘겨줌.
        result = {
            "ci_competition_rate": "",
            "ci_promise_content": "",
            "ci_promise_rate": 0.0,
        }
        return result


def scrape_ipostock(code):
    url = f"http://www.ipostock.co.kr/view_pg/view_05.asp?code={code}"

    from utilities import request_helper

    req = request_helper.requests_retry_session().get(url, timeout=5)
    soup = BeautifulSoup(req.content, "lxml", from_encoding="utf-8")
    table1_data = extract_data_from_table1(soup, url)
    table2_data = extract_data_from_table2(soup, url)

    return table1_data, table2_data


if __name__ == "__main__":
    code = "B202010131"
    prediction_result, general_result = scrape_ipostock(code)

    from schemas.general import GeneralCreateSchema
    from schemas.prediction import PredictionCreateSchema

    g = GeneralCreateSchema(**general_result)
    s = [PredictionCreateSchema(**data) for data in prediction_result or []]

    from pprint import pprint as pp

    # pp(g.dict())
    # pp(g.dict()["ci_competition_rate"])
    # pp(g.dict()["ci_promise_rate"])
    # pp(g.dict()["ci_promise_content"])
    si1 = s[0].dict()
    si2 = s[1].dict()
    si3 = s[2].dict()
    si4 = s[3].dict()
    print(si1)
    # print(si2)
    # print(si3)
    # print(si4)
