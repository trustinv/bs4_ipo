import aiohttp
import asyncio

import re
from datetime import datetime

import bs4
import requests
from bs4 import BeautifulSoup
from db.dals.company_dal import Company
from utilities.time_measure import timeit


시작년 = 2021
마지막년 = 2024
total = 0

ipo_companies = []
delisted_companies = []

공모철회회사수 = 0


async def delist(company_name):

    instance = Company()
    read, ci_demand_forcast_date = instance.read(company_name)

    # DB에는 공모철회가 없지만 공모철회로 데이터를 바꾸어야함.
    if read and ci_demand_forcast_date != "공모철회":
        delisted = instance.delist(company_name)


async def get_name_n_code(td_name):
    a_tag = td_name.select_one('a[href*="view_pg"][class=""]')
    href = a_tag["href"]
    company_code = re.search("code=(.+)&", href).group(1)
    company_name = a_tag.select_one("font").text.strip().replace(".", "")
    return company_code, company_name


async def get_years(year):
    current_year = datetime.now().year
    for k in range(year, current_year + 1):
        yield k


async def scrape_company_codes(year=2021):

    async for year in get_years(year):
        # ipo_companies_in_year = 0
        # delisted_companies_in_year = 0
        # print('*'*100)
        # print(f"year: {year}")
        page_data = None
        page = 1
        while page_data is None:
            ipo_companies_in_page = 0
            delisted_companies_in_page = 0
            url = f"http://www.ipostock.co.kr/sub03/ipo02.asp?str4={year}&str5=all&page={page}"
            # print(f"page: {page}, url: {url}")
            page += 1

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        soup = BeautifulSoup(await resp.text(), "lxml")

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print("Request failed, retrying in 5 seconds...")
                print(e)
                await asyncio.sleep(0.3)

            page_data = soup.select_one('td[colspan="9"]')
            if page_data is not None:
                break
            table = soup.select_one(
                "#print > table >  tr:nth-child(4) > td > table >  tr:nth-child(3) > td > table >  tr:nth-child(4) > td > table"
            )

            for idx, tr in enumerate(table, 1):
                if isinstance(tr, bs4.element.Tag):
                    td = tr.find("td", {"width": "120"})

                    if td is not None:
                        td_name = tr.find("td", {"width": "*"})
                        delisting = td.text.strip()
                        company_code, company_name = await get_name_n_code(td_name)

                        if delisting == "공모철회":
                            company = dict(
                                delistted_company_name=company_name,
                                delistted_company_code=company_code,
                            )
                            # print(company)
                            delisted_companies.append(company)
                            delisted_companies_in_page += 1

                        else:
                            company = dict(
                                ipo_company_name=company_name, ipo_company_code=company_code
                            )
                            # print(company)
                            ipo_companies.append(company)
                            ipo_companies_in_page += 1

    ipo_companies_codes = [
        value
        for ipo_company in ipo_companies
        for key, value in ipo_company.items()
        if key == "ipo_company_code"
    ]
    delisted_companies_codes = [
        value
        for delisted_company in delisted_companies
        for key, value in delisted_company.items()
        if key == "delistted_company_code"
    ]
    return ipo_companies_codes + delisted_companies_codes


if __name__ == "__main__":

    @timeit
    async def main():
        result = await scrape_company_codes()
        print(len(result))

    asyncio.run(main())
