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
        print("*" * 100)
        print(url)
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


def extract_data_from_table2(soup):
    keys = ["ci_competition_rate", "ci_promise_content"]
    results = []
    table = soup.find_all("table", width="780", cellspacing="1", class_="view_tb2")[-1]
    trs = table.select("tr")
    for tr in trs:
        tds = tr.select("td")
        for idx, td in enumerate(tds, 1):
            if idx % 2 == 0:
                results.append(td.text.strip())
    results = dict(zip(keys, results))
    return results


def scrape_ipostock(code):
    url = f"http://www.ipostock.co.kr/view_pg/view_05.asp?code={code}"

    from utilities import request_helper

    req = request_helper.requests_retry_session().get(url, timeout=5)
    soup = BeautifulSoup(req.content, "lxml", from_encoding="utf-8")
    table1_data = extract_data_from_table1(soup, url)
    table2_data = extract_data_from_table2(soup)

    return table1_data, table2_data


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_05.asp?code=B202206162&gmenu="
    prediction_result, general_result = scrape_ipostock(url)

    from schemas.general import GeneralCreateSchema
    from schemas.prediction import PredictionCreateSchema

    g = GeneralCreateSchema(**general_result)
    s = [PredictionCreateSchema(**data) for data in prediction_result]

    from pprint import pprint as pp

    # pp(g.dict())
    pp(s[0].dict())
