import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from agents import get_user_agents
from utilities.time_measure import timeit


# @timeit
def scrape_company_codes(year=2021):

    current_year = datetime.now().year
    codes = []
    for year in range(year, current_year + 1):
        # '리스트가 없습니다.'라는 colspan=9 속성이 안나올때까지 순회하게 됨.
        page_data = None
        page = 1
        while page_data is None:
            url = f"http://www.ipostock.co.kr/sub03/ipo02.asp?str4={year}&str5=all&page={page}"
            page += 1

            from utilities import request_helper

            req = request_helper.requests_retry_session().get(url, timeout=5)
            soup = BeautifulSoup(req.content, "lxml", from_encoding="utf-8")

            page_data = soup.select_one('td[colspan="9"]')
            if page_data is not None:
                break

            a_tags = soup.select('a[href*="view_pg"][class=""]')

            for tag in a_tags:
                href = tag["href"]
                code = re.search("code=(.+)&", href).group(1)
                codes.append(code)
    return codes


if __name__ == "__main__":
    result = scrape_company_codes()
