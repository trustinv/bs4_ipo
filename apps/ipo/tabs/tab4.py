from typing import List, Dict, Union, Optional
import asyncio
import aiohttp
import re

from bs4 import BeautifulSoup
from async_retrying import retry

from apps.ipo.agents import get_user_agents


async def cancelled_ipo(value: Optional[str]) -> Optional[str]:
    pass


async def extract_data_from_table1(table: BeautifulSoup) -> Dict[str, str]:
    """
    Extracts data from the first table in the HTML page and returns a dictionary with keys as the data categories
    and values as the data for each category.

    Parameters:
    - table (BeautifulSoup): The BeautifulSoup object representing the first table in the HTML page.

    Returns:
    - Dict[str, str]: A dictionary containing the extracted data.
    """
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


async def extract_data_from_table2(table: BeautifulSoup) -> Dict[str, str]:
    """
    Extracts data from the second table in the HTML page and returns a dictionary with keys as the data categories
    and values as the data for each category.

    Parameters:
    - table (BeautifulSoup): The BeautifulSoup object representing the second table in the HTML page.

    Returns:
    - Dict[str, str]: A dictionary containing the extracted data.
    """
    keys = [
        "ci_hope_po_price",
        "ci_hope_po_amount",
        "ci_confirm_po_price",
        "ci_confirm_po_amount",
        "ci_subscription_warrant_money_rate",
        "ci_subscription_competition_rate",
    ]
    result = []
    for idx, tr in enumerate(table, 1):
        if idx % 2 == 0:
            tds = tr.select("td")
            for jdx, td in enumerate(tds):
                if jdx % 2 == 1:
                    result.append(td.text)
    result = dict(zip(keys, result))
    return result


async def extract_data_from_table3(table: BeautifulSoup) -> Dict[str, str]:
    """
    Extracts data from the third table in the HTML page and returns a dictionary with keys as the data categories
    and values as the data for each category.

    Parameters:
    - table (BeautifulSoup): The BeautifulSoup object representing the third table in the HTML page.

    Returns:
    - Dict[str, str]: A dictionary containing the extracted data.
    """
    ci_public_offering_stocks, *rest_trs = table.select("tr")
    instance = ci_public_offering_stocks.select_one("td:nth-child(2) > b")
    data = None
    ci_public_offering_stocks = 0
    if instance is None:
        pass
    else:
        data = instance.get_text().split("주")[0]
        if data == "":
            pass
        ci_public_offering_stocks = f"{data}주"

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
    for tr in rest_trs:
        tds = tr.select("td")
        for td in tds:
            if re.search(r"\d+[,\d+]*", td.text):
                result.append(td.text)
    result = {key: value for key, value in zip(keys, result)}
    result.update(dict(ci_public_offering_stocks=ci_public_offering_stocks))
    return result


async def extract_data_from_table4(table: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Extracts data from the fourth table in the HTML page and returns a list of dictionaries, where each dictionary
    represents a row of data, with keys as the data categories and values as the data for each category.

    Parameters:
    - table (BeautifulSoup): The BeautifulSoup object representing the fourth table in the HTML page.

    Returns:
    - List[Dict[str, str]]: A list of dictionaries containing the extracted data.
    """
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


@retry(attempts=100)
async def scrape_ipostock(code: str) -> Dict[str, Union[str, Dict[str, str], List[Dict[str, str]]]]:
    """
    Scrapes financial data for a given company code from the website ipostock.co.kr.

    Parameters:
    - code (str): The company code to scrape financial data for.

    Returns:
    - Dict[str, Union[str, Dict[str, str], List[Dict[str, str]]]]: A dictionary containing the scraped financial data.
    """
    header = await get_user_agents()
    url = f"http://www.ipostock.co.kr/view_pg/view_04.asp?code={code}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=header) as resp:
                soup = BeautifulSoup(await resp.text(), "lxml")
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print("Request failed, retrying in 5 seconds...")
        print(e)
        await asyncio.sleep(1)

    table1, table2, table3, table4, *_ = soup.select("table.view_tb")

    t1, t2, t3, t4 = await asyncio.gather(
        extract_data_from_table1(table1),
        extract_data_from_table2(table2),
        extract_data_from_table3(table3),
        extract_data_from_table4(table4),
    )

    cancelled_ipo_css_selector = "#print > table > tr:nth-child(3) > td > table > tr > td:nth-child(1) > table > tr:nth-child(1) > td > table > tr > td:nth-child(2) > font > b"
    cancelled_ipo = soup.select_one(cancelled_ipo_css_selector)
    if not cancelled_ipo:
        is_cancelled = None
    else:
        is_cancelled = re.search(r"\[([^]]*)\]", cancelled_ipo.text)
        cancelled_ipo_text = is_cancelled.group(1)
        print(cancelled_ipo_text)
        t1 = {key: cancelled_ipo_text for key in t1}
    return {**t1, **t2, **t3}, t4


if __name__ == "__main__":

    async def main():

        code = "B202010131"

        code = "B202010131"
        general_result, subscriber_results = await scrape_ipostock(code)
        from pprint import pprint as pp

        print(general_result)
        # pp(subscriber_results)
        from schemas.general import GeneralCreateSchema
        from schemas.subscriber import SubscriberCreateSchema

        g = GeneralCreateSchema(**general_result)
        s = [
            SubscriberCreateSchema(**subscriber_result) for subscriber_result in subscriber_results
        ]

        from pprint import pprint as pp

        # print(g)
        # print(s)
        # gi = g.dict()
        # print(gi["ci_demand_forecast_date"])
        # print(gi["ci_appraised_price"])
        # pp(s)

    asyncio.run(main())
