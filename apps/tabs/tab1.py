import asyncio
import aiohttp
from bs4 import BeautifulSoup
from apps.agents import get_user_agents


async def face_value(soup):
    ci_face_value = None
    tds = soup.select('table[width="390"] td')
    for idx, td in enumerate(tds):
        font = td.select_one("font")
        if font and font.get_text() == "액면가":
            ci_face_value = tds[idx + 1].get_text().replace("원", "").replace(",", "").strip()
            break
    return ci_face_value or "0"


async def extract_data_from_table1(table):
    data2 = table.select_one(".view_tit").get_text()
    data3 = table.select_one(".view_txt01").get_text()
    data1 = table.select_one("img")["src"]
    return {"ci_market_separation": data1, "ci_name": data2, "ci_code": data3}


async def extract_data_from_table2(table):
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
    for idx_tr, tr in enumerate(trs):
        tds = tr.select("td.txt")
        result.extend(td.text if td.text is not None else "" for td in tds)
    result = dict(zip(keys, result))
    return result


async def extract_data_from_table3(table):
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
        "ci_public_offering_stocks",
        "ci_po_expected_amount",
        "ci_listing_expected_stocks",
    ]
    tds = table.select('tr > td[width="240"]')
    result = [td.text if td.text is not None else "" for td in tds]
    result = dict(zip(keys, result))
    return result


async def scrape_ipostock(code):
    header = await get_user_agents()
    url = f"http://www.ipostock.co.kr/view_pg/view_01.asp?code={code}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=header) as resp:
                soup = BeautifulSoup(await resp.text(), "lxml")
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print("Request failed, retrying in 5 seconds...")
        print(e)
        await asyncio.sleep(0.3)

    table1 = soup.find("table", width="550", style="margin:0 auto;")
    table2, table3 = soup.select('table[width="780"][class="view_tb"]')

    face_value_result, t1, t2, t3 = await asyncio.gather(
        face_value(soup),
        extract_data_from_table1(table1),
        extract_data_from_table2(table2),
        extract_data_from_table3(table3),
    )

    result = {"ci_face_value": face_value_result, **t1, **t2, **t3}
    return result


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
