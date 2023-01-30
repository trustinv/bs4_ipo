from typing import Dict, Union

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from async_retrying import retry
from apps.ipo.agents import get_user_agents
from config.config_log import logging

logger = logging.getLogger("info-logger")


async def face_value(soup: BeautifulSoup) -> str:
    """
    Returns the face value of a stock from the given BeautifulSoup object
    """
    ci_face_value = None
    tds = soup.select('table[width="390"] td')
    if not tds:
        logger.error("액면가를 가져 올수 없습니다. html tag를 확인하세요.")
    for idx, td in enumerate(tds):
        font = td.select_one("font")
        if font and font.get_text() == "액면가":
            ci_face_value = tds[idx + 1].get_text().replace("원", "").replace(",", "").strip()
            break
    return ci_face_value or "0"


async def extract_data_from_table1(table: BeautifulSoup) -> Dict[str, Union[str, int]]:
    """
    Extracts data from the first table of the provided BeautifulSoup object and returns a dictionary
    """
    try:
        data2 = table.select_one(".view_tit").get_text()
        data3 = table.select_one(".view_txt01").get_text()
        data1 = table.select_one("img")["src"]
        return {
            "ci_market_separation": data1,
            "ci_list_type": data1,
            "ci_name": data2,
            "ci_code": data3,
        }
    except KeyError as err:
        logger.error(err)
    except AttributeError as err:
        logger.error(err)


async def extract_data_from_table2(table: BeautifulSoup) -> Dict[str, str]:
    """
    Extracts data from the second table of the provided BeautifulSoup object and returns a dictionary
    """
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
    try:
        if not trs:
            logger.error("html 태그에 접근 할 수 없습니다.")
        for tr in trs:
            tds = tr.select("td.txt")
            result.extend(td.text if td.text is not None else "" for td in tds)
        result = dict(zip(keys, result))
        return result
    except AttributeError as err:
        logger.error(err)


async def extract_data_from_table3(table: BeautifulSoup) -> Dict[str, str]:
    """
    Extracts data from the third table of the provided BeautifulSoup object and returns a dictionary
    """
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
        "ci_po_expected_stocks",
        "ci_po_expected_amount",
        "ci_listing_expected_stocks",
    ]
    try:
        tds = table.select('tr > td[width="240"]')
        result = [td.string.strip() if td.string is not None else "" for td in tds]
        result = dict(zip(keys, result))
        return result
    except AttributeError as err:
        logger.error(err)


@retry(attempts=100)
async def scrape_ipostock(code: str) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Scrapes data from ipostock website using the provided code and returns a dictionary of the extracted data
    """
    header = await get_user_agents()
    url = f"http://www.ipostock.co.kr/view_pg/view_01.asp?code={code}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=header) as resp:
                soup = BeautifulSoup(await resp.text(), "lxml")

        table1 = soup.find("table", width="550", style="margin:0 auto;")
        table2, table3 = soup.select('table[width="780"][class="view_tb"]')

        if not table1 or not table2 or not table3:
            logger.error("html 태그 속성을 통해 데이터를 파싱 할 수 없습니다. ")

        face_value_result, t1, t2, t3 = await asyncio.gather(
            face_value(soup),
            extract_data_from_table1(table1),
            extract_data_from_table2(table2),
            extract_data_from_table3(table3),
        )

        result = {"ci_face_value": face_value_result, **t1, **t2, **t3}
        return result
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logger.error("Request failed, retrying in 5 seconds...")
        logger.error(e)
        await asyncio.sleep(1)


if __name__ == "__main__":

    async def main():
        code = "B202111241"
        result = await scrape_ipostock(code)

        # print(result["ci_public_offering_stocks"])

        from schemas.general import GeneralCreateSchema

        g = GeneralCreateSchema(**result)
        from pprint import pprint as pp

        inst = g.dict()
        pp(inst)
        # pp(inst["ci_face_value"])
        # pp(inst["ci_public_offering_stocks"])

    asyncio.run(main())
