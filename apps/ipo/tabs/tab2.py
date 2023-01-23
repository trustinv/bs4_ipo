import string
import asyncio
import aiohttp

from bs4 import BeautifulSoup
from apps.ipo.agents import get_user_agents
from config.config_log import logging

logger = logging.getLogger("info-logger")


async def get_capital_n_stcks(table):
    try:
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
    except AttributeError as err:
        logger.error(err)


async def extract_data_from_table1(table):
    capital, stocks = await get_capital_n_stcks(table)
    return dict(ci_before_po_capital=capital, ci_before_po_stocks=stocks)


async def extract_data_from_table2(table):
    capital, stocks = await get_capital_n_stcks(table)
    return dict(ci_after_po_capital=capital, ci_after_po_stocks=stocks)


async def convert_ci_current_ratio(value):
    try:
        if value is None or value in string.whitespace:
            return 0
        else:
            value = value.split(".")[0].replace(" ", "").strip()
            return int(value)
    except AttributeError as err:
        logger.error(err)


async def extract_data_from_table3(table):
    try:
        ci_current_ratio = table.select("tr")[-2].select_one("td:nth-child(4) > b").text

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
        for raw in tds[1:]:
            raw_text = raw.text.replace(" ", "").strip()
            if not raw_text:
                break
            # break
            if flag == 1:
                if "유통가능" in raw_text:
                    flag = 2
                    continue
                categories1.append(raw_text)
            else:
                categories2.append(raw_text)

        async def nesten_list(temp):
            return list(map(list, zip(*[iter(temp)] * 5)))

        temp3 = await nesten_list(categories1)
        temp4 = await nesten_list(categories2)
        for raw in temp3:
            raw.insert(0, 1)
        for raw in temp4:
            raw.insert(0, 2)
        result = [dict(zip(keys, lst)) for lst in temp3 + temp4]
        return result, dict(ci_current_ratio=ci_current_ratio)
    except AttributeError as err:
        logger.error(err)


async def scrape_ipostock(code):
    header = await get_user_agents()
    url = f"http://www.ipostock.co.kr/view_pg/view_02.asp?code={code}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=header) as resp:
                soup = BeautifulSoup(await resp.text(), "lxml")
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logger.error("Request failed, retrying in 5 seconds...")
        logger.error(e)
        await asyncio.sleep(0.3)

    table1, table2, table3 = soup.find_all("table", class_="view_tb")[:3]

    t1, t2, t3, = await asyncio.gather(
        extract_data_from_table1(table1),
        extract_data_from_table2(table2),
        extract_data_from_table3(table3),
    )
    t3, ci_current_ratio = t3
    return {**t1, **t2, **ci_current_ratio}, t3


if __name__ == "__main__":

    async def main():
        #        code = "B202111241"
        code = "B202109161"
        code = "B202207081"
        general_result, shareholder_results = await scrape_ipostock(code)
        from schemas.general import GeneralCreateSchema
        from schemas.shareholder import ShareholderCreateSchema

        g = GeneralCreateSchema(**general_result)
        s = [ShareholderCreateSchema(**shareholder) for shareholder in shareholder_results]

        # pp(g.dict())
        for i in s:
            print(i)

    asyncio.run(main(), debug=True)
