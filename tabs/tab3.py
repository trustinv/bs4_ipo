import aiohttp
import asyncio
import math
import pandas as pd


async def scrape_ipostock(code):
    print("tab3 company code", code)
    url = f"http://www.ipostock.co.kr/view_pg/view_03.asp?code={code}"
    keys = [
        "ci_category1",
        "ci_category2",
        "ci_current_asset",
        "ci_non_current_asset",
        "ci_current_liability",
        "ci_non_current_liability",
        "ci_capital",
        "ci_capital_surplus",
        "ci_earned_surplus",
        "ci_other_capital_items",
        "ci_turnover",
        "ci_business_profits",
        "ci_net_income",
    ]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.text()

    df = pd.read_html(data)
    df1 = df[21]
    구분 = df1.iloc[0, 0]

    if 구분 != "구분":
        print("There are NaN values in the DataFrame.")
        df1 = df[22]

    df1 = df1[~df1[0].isin(["자산총계", "부채총계", "자본총계"])]
    df1 = df1.iloc[:, 1:4]
    df1 = df1.dropna(axis=1, thresh=1, subset=[0])

    df_str = df1.iloc[:2, :]
    df2 = df1.loc[2:, :].astype("float")
    result = pd.concat([df_str, df2])
    df3 = result.T.values
    temp_data = []
    for data_row in df3:
        data_instance = {}

        for key, value in zip(keys, data_row):
            # print(key, value)
            if isinstance(value, float):
                if math.isnan(value):
                    processed_value = format(value, ".2f")
                else:
                    processed_value = format(value / (10e7), ".2f")
            else:
                processed_value = value
            data_instance[key] = processed_value
        temp_data.append(data_instance)
    return temp_data


if __name__ == "__main__":

    async def main():

        code = "B202111122"
        # code = "B201203062"
        code = "B201203062"

        financial_result = await scrape_ipostock(code)

        from pprint import pprint as pp

        pp(financial_result)
        # pp(financial_result[1])
        # pp(financial_result[0])
        # pp(financial_result[1])
        # pp(financial_result[2])
        # from schemas.financial import FinancialCreateSchema

        # s = [FinancialCreateSchema(**shareholder) for shareholder in financial_result]
        # print(s)

    asyncio.run(main())
