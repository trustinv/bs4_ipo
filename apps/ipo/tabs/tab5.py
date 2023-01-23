import asyncio
import aiohttp

from bs4 import BeautifulSoup
from apps.ipo.agents import get_user_agents


async def extract_data_from_table1(soup):
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
            empty_string = tds[0].text.strip().replace(" ", "")
            if not empty_string:
                break
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


async def extract_data_from_table2(soup):
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


async def scrape_ipostock(code):
    url = f"http://www.ipostock.co.kr/view_pg/view_05.asp?code={code}"
    header = await get_user_agents()
    try:
        async with aiohttp.ClientSession() as session:

            async with session.get(url, headers=header) as resp:
                soup = BeautifulSoup(await resp.text(), "lxml")
            soup = BeautifulSoup(await resp.text(), "lxml")
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print("Request failed, retrying in 5 seconds...")
        print(e)
        await asyncio.sleep(0.3)

    t1, t2 = await asyncio.gather(
        extract_data_from_table1(soup),
        extract_data_from_table2(soup),
    )

    return t1, t2


if __name__ == "__main__":

    async def main():

        #        code = "B202010131"
        # code = "B202010131"
        code = "B202105031"
        prediction_result, general_result = await scrape_ipostock(code)

        from schemas.general import GeneralCreateSchema
        from schemas.prediction import PredictionCreateSchema

        g = GeneralCreateSchema(**general_result)
        s = [PredictionCreateSchema(**data) for data in prediction_result or []]

        # print(g)
        # print(s)
        # from pprint import pprint as pp

        # # pp(g.dict())
        # # pp(g.dict()["ci_competition_rate"])
        # # pp(g.dict()["ci_promise_rate"])
        # # pp(g.dict()["ci_promise_content"])
        # si1 = s[0].dict()
        # si2 = s[1].dict()
        # si3 = s[2].dict()
        # si4 = s[3].dict()
        # print(si1)
        # print(si2)
        # print(si3)
        # print(si4)

    asyncio.run(main())
