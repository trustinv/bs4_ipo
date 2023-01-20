import time
import re
from datetime import datetime

import bs4
import requests
from db.dbmanager import DBManager
from utilities import request_helper


def delist(td_name, delisted_codes):
    company_name = (
        td_name.select_one("table > tr > td:nth-child(2) > a > font").text.strip().replace(".", "")
    )
    instance = DBManager()
    if isinstance(company_name, str) and len(company_name) > 2:
        delisted_codes.append(td_name)
        read, ci_demand_forcast_date = instance.read(company_name)

        # DB에는 공모철회가 없지만 공모철회로 데이터를 바꾸어야함.
        if read and ci_demand_forcast_date != "공모철회":
            delisted = instance.delist(company_name)


def get_href(td_name):
    a_tag = td_name.select_one('a[href*="view_pg"][class=""]')
    href = a_tag.get("href")
    code = re.search("code=(.+)&", href).group(1)
    return code


# @timeit
def scrape_company_codes(year=2021):

    current_year = datetime.now().year
    codes = []
    delisted_codes = []
    for year in range(year, current_year + 1):
        #
        #  '리스트가 없습니다.'라는 colspan=9 속성이 안나올때까지 순회하게 됨.
        print(f"year: {year}")
        page_data = None
        page = 1
        while page_data is None:
            print(f"page: {page}")
            page += 1
            url = f"http://www.ipostock.co.kr/sub03/ipo02.asp?str4={year}&str5=all&page={page}"

            session = requests.Session()
            session.timeout = 3
            while True:
                try:
                    req = session.get(url)
                    req.encoding = "utf-8"
                    print(req.text)
                    # req = requests.get(url)
                    soup = bs4.BeautifulSoup(req.content, "lxml")
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

            page_data = soup.select_one('td[colspan="9"]')
            if page_data is not None:
                break

            table = soup.select_one(
                "#print > table >  tr:nth-child(4) > td > table >  tr:nth-child(3) > td > table >  tr:nth-child(4) > td > table"
            )

            for tr in table:
                if isinstance(tr, bs4.element.Tag):
                    td = tr.find("td", {"width": "120"})

                    if td is not None:
                        delisting = td.text.strip()
                        td_name = tr.find("td", {"width": "*"})

                        if delisting == "공모철회":
                            if td_name is not None:
                                delist(td_name, delisted_codes)
                                # 성공적으로 종목을 공모 철회로 바꾼 경우.
                                # 이미 되어 있는 경우

                                # 회사 이름으로 쿼리 때려서 2가지로 나뉨
                                # 1) 반환 값이 공모철회(0) ->
                                # 2) 반환 값이 공모철회(X) -> ci_demand_forecast_? 를 공모철회로 변경
                        else:
                            codes.append(get_href(td_name))
    return codes, delisted_codes


if __name__ == "__main__":
    company_codes, delisted_codes = scrape_company_codes()
    print(len(company_codes), len(delisted_codes))
