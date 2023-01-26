import aiohttp
import asyncio

import re
from datetime import datetime

import bs4
from bs4 import BeautifulSoup
from db.config import async_session
from db.dals.company_dal import Company
from utilities.time_measure import timeit
from apps.ipo.agents import get_user_agents
from config.config_log import logging

logger = logging.getLogger("info-logger")


async def delist(session, company_name):

    instance = Company(session)
    read, ci_demand_forcast_date = instance.read(company_name)

    # DB에는 공모철회가 없지만 공모철회로 데이터를 바꾸어야함.
    if read and ci_demand_forcast_date != "공모철회":
        delisted = instance.delist(company_name)
        if delisted:
            logger.info("공모철회 한 회사 : {company_name}")


async def get_name_n_code(td_name):
    try:
        a_tag = td_name.select_one('a[href*="view_pg"][class=""]')
        href = a_tag["href"]
        company_code = re.search("code=(.+)&", href).group(1)
        company_name = a_tag.select_one("font").text.strip().replace(".", "")
        return company_code, company_name
    except KeyError as err:
        logger.error(err)
    except AttributeError as err:
        logger.error(err)


async def get_years(year):
    current_year = datetime.now().year
    for k in range(year, current_year + 1):
        yield k


from async_retrying import retry


@retry(attempts=100)
async def scrape_company_codes(year=2021):
    ipo_companies = []
    delisted_companies = []
    header = await get_user_agents()
    async for year in get_years(year):
        logger.debug("연도", year)
        page_data = None
        page = 1
        while page_data is None:
            ipo_companies_in_page = 0
            delisted_companies_in_page = 0
            url = f"http://www.ipostock.co.kr/sub03/ipo02.asp?str4={year}&str5=all&page={page}"
            logger.debug(f"page: {page}, url: {url}")
            page += 1

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=header) as resp:
                        soup = BeautifulSoup(await resp.text(), "lxml")

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print("Request failed, retrying in 5 seconds...")
                print(e)
                await asyncio.sleep(1)

            page_data = soup.select_one('td[colspan="9"]')
            if page_data is not None:
                logger.debug("페이지에 기업이 없습니다. 다음 연도로 전환됩니다")
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

                        # DB에 데이터가 없는 경우

                        if delisting == "공모철회":
                            company = dict(
                                delistted_company_name=company_name,
                                delistted_company_code=company_code,
                            )
                            # async with async_session() as session:
                            # async with session.begin():
                            # delist(session, company_name)
                            # pass
                            logger.info(f"공모철회 회사명 : {company_name}/ 코드:{company_code}")
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
    all_companies_codes = ipo_companies_codes + delisted_companies_codes
    logger.debug(f"모든 회사 코드: {all_companies_codes}")
    return all_companies_codes


if __name__ == "__main__":

    @timeit
    async def main():
        result = await scrape_company_codes()
        print(len(result))

    asyncio.run(main())
